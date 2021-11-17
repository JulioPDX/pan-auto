from panos import base
from panos import firewall
from panos import policies
from panos import objects
from panos import network
from panos import device
from rich import print, inspect


fw = firewall.Firewall("192.168.10.192", "admin", "PaloAlto123!")


# Creating Zones on firewall
lan_zone = network.Zone(
    name="User LAN",
    mode="layer3",
    zone_profile="DefaultZoneProtectionProfile",
    log_setting="Zone-Forwarding-Profile",
    enable_packet_buffer_protection=True,
)

fw.add(lan_zone)
lan_zone.create()


dc_zone = network.Zone(
    name="Datacenter",
    mode="layer3",
    zone_profile="DefaultZoneProtectionProfile",
    log_setting="Zone-Forwarding-Profile",
    enable_packet_buffer_protection=True,
)

fw.add(dc_zone)
dc_zone.create()


dmz_zone = network.Zone(
    name="DMZ",
    mode="layer3",
    zone_profile="DefaultZoneProtectionProfile",
    log_setting="Zone-Forwarding-Profile",
    enable_packet_buffer_protection=True,
)

fw.add(dmz_zone)
dmz_zone.create()


outside_zone = network.Zone(
    name="Outside",
    mode="layer3",
    zone_profile="OutsideZoneProtectionProfile",
    log_setting="Zone-Forwarding-Profile",
    enable_packet_buffer_protection=True,
)

fw.add(outside_zone)
outside_zone.create()


# Configuring main firewall interfaces
outside_intf = network.EthernetInterface(
    name="ethernet1/1",
    mode="layer3",
    link_state="up",
    comment="Outside",
    enable_dhcp=True,
    create_dhcp_default_route=True,
    management_profile="AllowPing",
)
fw.add(outside_intf)
outside_intf.set_zone("Outside")
outside_intf.set_virtual_router("default")
fw.add(outside_intf)

outside_intf.create()


dmz_intf = network.EthernetInterface(
    name="ethernet1/2",
    mode="layer3",
    link_state="up",
    comment="DMZ",
    ip=("10.100.100.1/24"),
    management_profile="AllowPing",
)
fw.add(dmz_intf)
dmz_intf.set_zone("DMZ")
dmz_intf.set_virtual_router("default")
fw.add(dmz_intf)

dmz_intf.create()


dc_intf = network.EthernetInterface(
    name="ethernet1/3",
    mode="layer3",
    link_state="up",
    comment="Datacenter",
    ip=("10.172.20.1/30"),
    management_profile="AllowPing",
)
fw.add(dc_intf)
dc_intf.set_zone("Datacenter")
dc_intf.set_virtual_router("default")
fw.add(dc_intf)

dc_intf.create()


lan_intf = network.EthernetInterface(
    name="ethernet1/4",
    mode="layer3",
    link_state="up",
    comment="LAN",
    ip=("10.17.5.1/30"),
    management_profile="AllowPing",
)
fw.add(lan_intf)
lan_intf.set_zone("User LAN")
lan_intf.set_virtual_router("default")
fw.add(lan_intf)

lan_intf.create()


# Standing up Virtual Router
vr_fw = network.VirtualRouter(
    name="default",
)
fw.add(vr_fw)
vr_fw.create()

# Redistribution Profile
redis = network.RedistributionProfile(
    name="DefaultRoute",
    priority=1,
    filter_type=("static"),
    action="redist",
)
vr_fw.add(redis)
redis.create()

# Configuring OSPF process
ospf_fw = network.Ospf(
    enable=True,
    reject_default_route=True,
    router_id="10.17.5.1",
    allow_redist_default_route=True,
)
vr_fw.add(ospf_fw)
ospf_fw.create()

ospf_area = network.OspfArea(
    name="0.0.0.0",
    type="normal",
)
ospf_fw.add(ospf_area)
ospf_area.create()

area_0_ranges = ["192.168.10.0/24", "10.100.100.0/24", "10.172.20.0/30", "10.17.5.0/30"]
for prefix in area_0_ranges:
    adver = network.OspfRange(name=prefix, mode="advertise")
    ospf_area.add(adver)
    adver.create()

area_0_interfaces = ["ethernet1/3", "ethernet1/4"]
for interface in area_0_interfaces:
    ospf_interface = network.OspfAreaInterface(name=interface, enable=True, link_type="broadcast")
    ospf_area.add(ospf_interface)
    ospf_interface.create()

ospf_export = network.OspfExportRules(
    name=redis,
    new_path_type="ext-2",
)
ospf_fw.add(ospf_export)
ospf_export.create()

print("[bold yellow]Committing configuration...[/bold yellow]")
print(fw.commit(sync=True))
print("[bold green]Complete...[/bold green]")
