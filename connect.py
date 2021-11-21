# from panos import base
from panos import firewall
from panos import policies
from panos import objects
from panos import network

# from panos import device
from rich import print, inspect
from rich.progress import Progress, SpinnerColumn, TextColumn


fw = firewall.Firewall("192.168.10.192", "admin", "PaloAlto123!")


# Creating Zones on Firewall
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


# Custom Tags
tags = {
    "any": {
        "color": "brown",
    },
    "User LAN": {
        "color": "green",
    },
    "DMZ": {
        "color": "yellow",
    },
    "Outside": {
        "color": "red",
    },
    "Datacenter": {
        "color": "blue gray",
    },
    "Internet Gateway": {
        "color": "cyan",
    },
    "Temporary": {
        "color": "black",
    },
    "IT": {
        "color": "light green",
    },
}

for k, v in tags.items():
    current_tag = objects.Tag(name=k, color=objects.Tag.color_code(v["color"]))
    fw.add(current_tag)
    current_tag.create()


# Configuring Main Firewall Interfaces
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


# Virtual Router
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
    ospf_interface = network.OspfAreaInterface(
        name=interface, enable=True, link_type="broadcast", passive=False
    )
    ospf_area.add(ospf_interface)
    ospf_interface.create()

area_0_interfaces_passive = ["ethernet1/2"]
for interface in area_0_interfaces_passive:
    ospf_interface = network.OspfAreaInterface(
        name=interface, enable=True, link_type="p2p", passive=True
    )
    ospf_area.add(ospf_interface)
    ospf_interface.create()

ospf_export = network.OspfExportRules(
    name=redis,
    new_path_type="ext-2",
)
ospf_fw.add(ospf_export)
ospf_export.create()


# Application Filters
# evasive_filter = objects.ApplicationFilter(name="Evasive Applications", evasive=True)
# fw.add(evasive_filter)
# evasive_filter.create()

# peer_to_peer_filter = objects.ApplicationFilter(
#     name="peer-to-peer", technology=["peer-to-peer"]
# )
# fw.add(peer_to_peer_filter)
# peer_to_peer_filter.create()

# encrypted_tunnels_filter = objects.ApplicationFilter(
#     name="encrypted-tunnels", subcategory=["encrypted-tunnel"]
# )
# fw.add(encrypted_tunnels_filter)
# encrypted_tunnels_filter.create()

# remote_access_filter = objects.ApplicationFilter(
#     name="remote-access", subcategory=["remote-access"]
# )
# fw.add(remote_access_filter)
# remote_access_filter.create()

# general_business_filter = objects.ApplicationFilter(
#     name="general-business",
#     category="business-systems",
#     subcategory=["general-business"],
# )
# fw.add(general_business_filter)
# general_business_filter.create()


# Application Groups
# denied_apps_group = objects.ApplicationGroup(
#     name="Denied Applications",
#     value=[
#         "Evasive Applications",
#         "peer-to-peer",
#         "encrypted-tunnels",
#         "remote-access",
#     ],
# )
# fw.add(denied_apps_group)
# denied_apps_group.create()

# sanctioned_saas_group = objects.ApplicationGroup(
#     name="Sanctioned SaaS",
#     value=["asana", "salesforce", "bloomberg-professional", "amazon-aws-console"],
# )
# fw.add(sanctioned_saas_group)
# sanctioned_saas_group.create()


# Custom App Example
# globo_web_app = objects.ApplicationObject(
#     name="Globo-Web-Front",
#     description="Some Fake Application",
#     category="business-systems",
#     subcategory="general-business",
#     technology="browser-based",
#     risk=3,
# )
# fw.add(globo_web_app)
# globo_web_app.create()


# Custom Service Object
# udp_80_service = objects.ServiceObject(
#     name="UDP_80", description="QUIC Port", protocol="udp", destination_port="80"
# )
# fw.add(udp_80_service)
# udp_80_service.create()

# udp_443_service = objects.ServiceObject(
#     name="UDP_443",
#     description="QUIC Port",
#     protocol="udp",
#     destination_port="443",
# )
# fw.add(udp_443_service)
# udp_443_service.create()


# Custom Service Group
# quic_service_group = objects.ServiceGroup(
#     name="QUIC_Ports", value=["UDP_80", "UDP_443"]
# )
# fw.add(quic_service_group)
# quic_service_group.create()


# print("[bold yellow]Committing configuration...[/bold yellow]")
# print(fw.commit(sync=True))
# print("[bold green]Please see committ output above...[/bold green]")


# Address objects
address_objects = {
    "Contractors": {
        "address": "10.17.11.0/24",
    },
    "Datacenter Applications": {
        "address": "10.172.22.0/24",
    },
    "Datacenter Infrastructure": {
        "address": "10.172.21.0/24",
    },
    "Datacenter Internal DNS": {
        "address": "10.172.21.5",
    },
    "OOBM": {
        "address": "172.20.1.0/24",
    },
    "Operations-Finance": {
        "address": "10.17.6.0/24",
    },
    "Operations-Sales": {
        "address": "10.17.8.0/24",
    },
    "IT Administrators": {
        "address": "10.17.7.0/24",
    },
    "IT Developers": {
        "address": "10.17.9.0/24",
    },
}
for k, v in address_objects.items():
    current_address = objects.AddressObject(
        name=k, value=v["address"], type="ip-netmask"
    )
    fw.add(current_address)
    current_address.create()


# Address Groups
it_users_group = objects.AddressGroup(
    name="IT Users", static_value=["IT Administrators", "IT Developers"], tag="User LAN"
)
fw.add(it_users_group)
it_users_group.create()

operations_user_group = objects.AddressGroup(
    name="Operations User Subnets",
    static_value=["Operations-Finance", "Operations-Sales"],
    tag="User LAN",
)
fw.add(operations_user_group)
operations_user_group.create()

datacenter_user_group = objects.AddressGroup(
    name="Datacenter Subnets",
    static_value=[
        "Datacenter Applications",
        "Datacenter Infrastructure",
        "Datacenter Internal DNS",
    ],
    tag="Datacenter",
)
fw.add(datacenter_user_group)
datacenter_user_group.create()

all_users_group = objects.AddressGroup(
    name="All User Subnets",
    static_value=["IT Users", "Operations User Subnets"],
    tag="User LAN",
)
fw.add(all_users_group)
all_users_group.create()


# Security Profile Groups
# Profiles must exist, did not find call to create
# individual security profiles
custom_spg = objects.SecurityProfileGroup(
    name="Internet Security Profile",
    virus="Strict_AV",
    spyware="BP_Spyware",
    vulnerability="BP_VPP",
    url_filtering="BP_URLFiltering",
    file_blocking="strict file blocking",
    data_filtering=None,
    wildfire_analysis="default",
)
fw.add(custom_spg)
custom_spg.create()


# Security Policies
## Instantiate the Rulebase
rulebase = policies.Rulebase()
fw.add(rulebase)

users_to_dns_policy = policies.SecurityRule(
    name="Users to Internal DNS Server",
    type="universal",
    description="Allows user LANs to communicate with internal DNS server",
    tag=["Internet Gateway"],
    fromzone=["User LAN"],
    source=["All User Subnets"],
    tozone=["Datacenter"],
    destination=["Datacenter Internal DNS"],
    application=["dns", "icmp", "ping"],
    action="allow",
    group="Internet Security Profile",
    log_end=True,
)
rulebase.add(users_to_dns_policy)
users_to_dns_policy.create()

dns_to_internet_policy = policies.SecurityRule(
    name="Internal DNS to Internet",
    type="universal",
    description="Allows internal DNS to communicate with Internet",
    fromzone=["Datacenter"],
    source=["Datacenter Internal DNS"],
    tozone=["Outside"],
    destination=["any"],
    application=["dns", "icmp", "ping"],
    action="allow",
    log_end=True,
)
rulebase.add(dns_to_internet_policy)
dns_to_internet_policy.create()

general_to_internet_policy = policies.SecurityRule(
    name="General Internet",
    type="universal",
    description="Allows users access to the Internet",
    tag=["Internet Gateway"],
    fromzone=["User LAN"],
    source=["All User Subnets"],
    tozone=["Outside"],
    destination=["any"],
    application=["web-browsing", "ssl", "icmp", "ping"],
    action="allow",
    group="Internet Security Profile",
    log_end=True,
)
rulebase.add(general_to_internet_policy)
general_to_internet_policy.create()


# Generic Outbound NAT for users
general_nat = policies.NatRule(
    name="General NAT",
    description="General NAT for internet access",
    nat_type="ipv4",
    tag=["Outside"],
    fromzone=["User LAN"],
    tozone=["Outside"],
    to_interface="ethernet1/1",
    source=["All User Subnets"],
    destination=["any"],
    source_translation_type="dynamic-ip-and-port",
    source_translation_address_type="interface-address",
    source_translation_interface="ethernet1/1",
    source_translation_ip_address=None,
    destination_translated_address=None,
    service="any",
)
rulebase.add(general_nat)
general_nat.create()


with Progress(
    SpinnerColumn("aesthetic", speed=0.4), TextColumn("{task.description}")
) as progress:

    task1 = progress.add_task("[bold yellow]Committing Configuration...", total=1)
    while not progress.finished:
        print(fw.commit(sync=True, exception=True))
        progress.update(task1, advance=1)
print("[bold green]Please see commit output above...[/bold green]")
