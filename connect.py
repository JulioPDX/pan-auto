from panos import base
from panos import firewall
from panos import policies
from panos import objects
from panos import network
from panos import device
from rich import print, inspect


fw = firewall.Firewall("192.168.10.192", "admin", "PaloAlto123!")

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

outside_intf = network.EthernetInterface(
    name="ethernet1/1",
    mode="layer3",
    link_state="up",
    comment="Outside",
    enable_dhcp=True,
    create_dhcp_default_route=True,
    management_profile="AllowPing"
)
fw.add(outside_intf)
setzone = outside_intf.set_zone("Outside")
setvr = outside_intf.set_virtual_router("default")
fw.add(setzone)
fw.add(setvr)

outside_intf.create()
setzone.create()
setvr.create()

dmz_intf = network.EthernetInterface(
    name="ethernet1/2",
    mode="layer3",
    link_state="up",
    comment="DMZ",
    ip=("10.100.100.1/24"),
    management_profile="AllowPing",
)
fw.add(dmz_intf)
dmz_setzone = dmz_intf.set_zone("DMZ")
dmz_setvr = dmz_intf.set_virtual_router("default")
fw.add(dmz_setzone)
fw.add(dmz_setvr)

dmz_intf.create()
dmz_setzone.create()
dmz_setvr.create()

dc_intf = network.EthernetInterface(
    name="ethernet1/3",
    mode="layer3",
    link_state="up",
    comment="Datacenter",
    ip=("10.172.20.1/30"),
    management_profile="AllowPing",
)
fw.add(dc_intf)
dc_setzone = dc_intf.set_zone("Datacenter")
dc_setvr = dc_intf.set_virtual_router("default")
fw.add(dc_setzone)
fw.add(dc_setvr)

dc_intf.create()
dc_setzone.create()
dc_setvr.create()

lan_intf = network.EthernetInterface(
    name="ethernet1/4",
    mode="layer3",
    link_state="up",
    comment="LAN",
    ip=("10.17.5.1/30"),
    management_profile="AllowPing",
)
fw.add(lan_intf)
lan_setzone = lan_intf.set_zone("User LAN")
lan_setvr = lan_intf.set_virtual_router("default")
fw.add(lan_setzone)
fw.add(lan_setvr)

lan_intf.create()
lan_setzone.create()
lan_setvr.create()

print("[bold green]Committing configuration...[/bold green]")
fw.commit(sync=True)
