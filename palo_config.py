#!/usr/bin/env python
"""
POC script used to configure a Palo Alto Firewall.
Config examples are based on the Pluralsight course by Craig Stansbury.
"""

from panos import firewall
from panos import policies
from panos import objects
from panos import network
from rich import print as rprint
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

# Firewall config imports
from configs.zones import zones
from configs.tags import tags
from configs.interfaces import interfaces
from configs.routing import routing
from configs.address_objects import address_objects
from configs.address_groups import address_groups
from configs.security_policies import security_policies
from configs.nats import nats


fw = firewall.Firewall("192.168.10.192", "admin", "PaloAlto123!")


def create_zone(fire, curent_zone):
    """Creates firewall zone and returns object"""
    set_zone = network.Zone(**curent_zone)
    fire.add(set_zone)
    set_zone.create()
    return set_zone


def create_tag(fire, current_tag):
    """Creates firewall tag and calls color_code to get numberical value"""
    set_tag = objects.Tag(
        name=current_tag["name"], color=objects.Tag.color_code(current_tag["color"])
    )
    fire.add(set_tag)
    set_tag.create()
    return set_tag


def create_interface(fire, current_int):
    """Creates interfaces and sets to proper VR and Zone, both must previoisly exist"""
    set_interface = network.EthernetInterface(**current_int["data"])
    fire.add(set_interface)
    set_interface.set_virtual_router(
        current_int["virtual_router"], update=True, refresh=True
    )
    set_interface.set_zone(current_int["zone"], update=True, refresh=True)
    fire.add(set_interface)
    set_interface.create()
    return set_interface


def create_virtual_router(fire, name):
    """Creates a virtual router instance"""
    v_router = network.VirtualRouter(name)
    fire.add(v_router)
    v_router.create()
    return v_router


def create_ospf_process(v_router, data):
    """Creates an OSPF process under a previously created virtual router instance"""
    ospf_process = network.Ospf(**data)
    v_router.add(ospf_process)
    ospf_process.create()
    return ospf_process


def create_redis_profile(v_router, data):
    """Creates redistribution profile under virtual router instance"""
    redis_profile = network.RedistributionProfile(**data)
    v_router.add(redis_profile)
    redis_profile.create()
    return redis_profile


def create_ospf_export_rule(ospf, name, path_type):
    """Creates OSPF export rules under OSPF process"""
    ospf_export = network.OspfExportRules(name=name, new_path_type=path_type)
    ospf.add(ospf_export)
    ospf_export.create()
    return ospf_export


def create_ospf_area(ospf, data):
    """Creates OSPF area under an OSPF process"""
    ospf_area = network.OspfArea(**data)
    ospf.add(ospf_area)
    ospf_area.create()
    return ospf_area


def create_ospf_range(ospf_area, data):
    """Creates OSPF range under an OSPF process"""
    adver_range = network.OspfRange(**data)
    ospf_area.add(adver_range)
    adver_range.create()
    return adver_range


def create_ospf_interface(ospf_area, data):
    """Sets interface to be advertised under OSPF area"""
    ospf_interface = network.OspfAreaInterface(**data)
    ospf_area.add(ospf_interface)
    ospf_interface.create()
    return ospf_interface


def create_address_object(fire, data):
    """Creates individual address objects under firewall instance"""
    a_object = objects.AddressObject(**data)
    fire.add(a_object)
    a_object.create()
    return a_object


def create_address_group(fire, data):
    """Creates address group against address object (must exist)"""
    a_group = objects.AddressGroup(**data)
    fire.add(a_group)
    a_group.create()
    return a_group


def create_security_policy(fire, data):
    """Creates security policies and adds to rulebase"""
    rulebase = policies.Rulebase()
    fire.add(rulebase)
    s_group = policies.SecurityRule(**data)
    rulebase.add(s_group)
    s_group.create()
    return s_group


def create_nat_rule(fire, data):
    """Creates NAT rules and adds to rulebase"""
    rulebase = policies.Rulebase()
    fire.add(rulebase)
    nat = policies.NatRule(**data)
    rulebase.add(nat)
    nat.create()
    return nat


with Progress(
    SpinnerColumn("bouncingBall", speed=0.6),
    BarColumn(),
    TextColumn("[progress.percentage]{task.description} {task.percentage:>3.0f}%"),
) as progress:
    job1 = progress.add_task("[bright_green]Configuring Zones", total=len(zones))
    job2 = progress.add_task("[bright_magenta]Configuring Tags", total=len(tags))
    job3 = progress.add_task(
        "[bright_cyan]Configuring Interfaces", total=len(interfaces)
    )
    job4 = progress.add_task(
        "[dark_sea_green2]Configuring Virtual Routers", total=len(routing)
    )
    job5 = progress.add_task("[bright_yellow]Configuring OSPF Process", total=1)
    job6 = progress.add_task("[sky_blue1]Configuring Redistribution Profiles", total=1)
    job7 = progress.add_task("[indian_red]Configuring OSPF Export Rules", total=1)
    job8 = progress.add_task("[thistle1]Configuring OSPF Areas", total=1)
    job9 = progress.add_task("[light_steel_blue]Configuring OSPF Ranges", total=4)
    job10 = progress.add_task("[wheat1]Configuring OSPF Interfaces", total=3)
    job11 = progress.add_task(
        "[grey100]Configuring Address Objects", total=len(address_objects)
    )
    job12 = progress.add_task(
        "[pink3]Configuring Address Groups", total=len(address_groups)
    )
    job13 = progress.add_task(
        "[dark_sea_green2]Configuring Security Policies", total=len(security_policies)
    )
    job14 = progress.add_task("[aquamarine1]Configuring NAT Rules", total=len(nats))
    final = progress.add_task("[bold yellow]Committing Configuration...", total=1)

    while not progress.finished:
        # Configuring high level settings. Logic may need to change if
        # you are not using the default virtual router
        for zone in zones:
            create_zone(fw, zone)
            progress.update(job1, advance=1)
        for tag in tags:
            create_tag(fw, tag)
            progress.update(job2, advance=1)
        for interface in interfaces:
            create_interface(fw, interface)
            progress.update(job3, advance=1)

        # Configuring Routing
        for router in routing:
            current_router = create_virtual_router(fw, router["virtual_router"])
            progress.update(job4, advance=1)
            if router["ospf"]:
                local_ospf = create_ospf_process(current_router, router["ospf"]["data"])
                progress.update(job5, advance=1)

            # Configuring any redistribution profiles tied to router instance
            for redis in router["ospf"]["redis_profiles"]:
                rp = create_redis_profile(current_router, redis["data"])
                progress.update(job6, advance=1)
                if redis["ospf_export_rules"]:
                    for rule in redis["ospf_export_rules"]:
                        export = create_ospf_export_rule(
                            local_ospf, rp, rule["new_path_type"]
                        )
                        progress.update(job7, advance=1)

            # Configuring all OSPF settings under router instance
            for area in router["ospf"]["areas"]:
                current_area = create_ospf_area(local_ospf, area["data"])
                progress.update(job8, advance=1)
                for area_range in area["ranges"]:
                    current_range = create_ospf_range(current_area, area_range)
                    progress.update(job9, advance=1)
                for interface in area["interfaces"]:
                    current_interface = create_ospf_interface(current_area, interface)
                    progress.update(job10, advance=1)

            for address in address_objects:
                current_address = create_address_object(fw, address)
                progress.update(job11, advance=1)

            for group in address_groups:
                current_group = create_address_group(fw, group)
                progress.update(job12, advance=1)

            for policy in security_policies:
                current_policy = create_security_policy(fw, policy)
                progress.update(job13, advance=1)

            for nat_rule in nats:
                current_nat = create_nat_rule(fw, nat_rule)
                progress.update(job14, advance=1)

            commit = fw.commit(sync=True, exception=True)
            progress.update(final, advance=1)
            # rprint("[bold green]Please see commit output below...[/bold green]")
rprint(commit)
