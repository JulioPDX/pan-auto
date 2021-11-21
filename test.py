from panos import firewall
from panos import policies
from panos import objects
from panos import network
from rich import print, inspect
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn


# Firewall config imports
from configs.zones import zones
from configs.tags import tags
from configs.interfaces import interfaces
from configs.routing import routing


fw = firewall.Firewall("192.168.10.192", "admin", "PaloAlto123!")


def create_zones(fw, curent_zone):
    set_zone = network.Zone(**curent_zone)
    fw.add(set_zone)
    set_zone.create()
    return set_zone


def create_tags(fw, current_tag):
    set_tag = objects.Tag(
        name=current_tag["name"], color=objects.Tag.color_code(current_tag["color"])
    )
    fw.add(set_tag)
    set_tag.create()
    return set_tag


def create_interfaces(fw, current_interface):
    set_interface = network.EthernetInterface(**current_interface["data"])
    fw.add(set_interface)
    set_interface.set_virtual_router("default", update=True, refresh=True)
    set_interface.set_zone("Outside", update=True, refresh=True)
    fw.add(set_interface)
    set_interface.create()
    return set_interface


def create_virtual_router(fw, name):
    vr = network.VirtualRouter(name)
    fw.add(vr)
    vr.create()
    return vr


def create_ospf_process(vr, data):
    ospf_process = network.Ospf(**data)
    vr.add(ospf_process)
    ospf_process.create()
    return ospf_process


def create_redis_profile(vr, data):
    redis = network.RedistributionProfile(**data)
    vr.add(redis)
    redis.create()
    return redis


def create_ospf_export_rule(ospf, name, type):
    ospf_export = network.OspfExportRules(name=name, new_path_type=type)
    ospf.add(ospf_export)
    ospf_export.create()
    return ospf_export


def create_ospf_area(ospf, data):
    ospf_area = network.OspfArea(**data)
    ospf.add(ospf_area)
    ospf_area.create()
    return ospf_area


def create_ospf_range(ospf_area, data):
    adver_range = network.OspfRange(**data)
    ospf_area.add(adver_range)
    adver_range.create()
    return adver_range


def create_ospf_interface(ospf_area, data):
    ospf_interface = network.OspfAreaInterface(**data)
    ospf_area.add(ospf_interface)
    ospf_interface.create()
    return ospf_interface


# for zone in zones:
#     create_zones(fw, zone)

# for tag in tags:
#     create_tags(fw, tag)

# for interface in interfaces:
#     create_interfaces(fw, interface)


with Progress(
    SpinnerColumn(),
    BarColumn(),
    TextColumn("[progress.percentage]{task.description} {task.percentage:>3.0f}%"),
) as progress:
    job1 = progress.add_task("[green]Configuring Zones", total=len(zones))
    job2 = progress.add_task("[magenta]Configuring Tags", total=len(tags))
    job3 = progress.add_task("[cyan]Configuring Interfaces", total=len(interfaces))
    # job4 = progress.add_task("[cyan]Configuring Virtual Router", total=len(routing))
    # job5 = progress.add_task("[cyan]Configuring OSPF Process", total=len(interfaces))
    # job6 = progress.add_task("[cyan]Configuring Redistribution Profiles", total=len(interfaces))
    # job7 = progress.add_task("[cyan]Configuring OSPF Export Rules", total=len(interfaces))
    # job8 = progress.add_task("[cyan]Configuring OSPF Areas", total=len(interfaces))
    # job9 = progress.add_task("[cyan]Configuring OSPF Ranges", total=len(interfaces))
    # job10 = progress.add_task("[cyan]Configuring OSPF Interfaces", total=len(interfaces))


    while not progress.finished:
        for zone in zones:
            create_zones(fw, zone)
            progress.update(job1, advance=1)
        for tag in tags:
            create_tags(fw, tag)
            progress.update(job2, advance=1)
        for interface in interfaces:
            create_interfaces(fw, interface)
            progress.update(job3, advance=1)


# Configuring Routing
for router in routing:
    current_router = create_virtual_router(fw, router["virtual_router"])
    if router["ospf"]:
        local_ospf = create_ospf_process(current_router, router["ospf"]["data"])

    # Configuring any redistribution profiles tied to router instance
    for redis in router["ospf"]["redis_profiles"]:
        rp = create_redis_profile(current_router, redis["data"])
        if redis["ospf_export_rules"]:
            for rule in redis["ospf_export_rules"]:
                export = create_ospf_export_rule(local_ospf, rp, rule["new_path_type"])

    # Configuring all OSPF settings under router instance
    for area in router["ospf"]["areas"]:
        current_area = create_ospf_area(local_ospf, area["data"])
        for range in area["ranges"]:
            current_range = create_ospf_range(current_area, range)
        for interface in area["interfaces"]:
            current_interface = create_ospf_interface(current_area, interface)