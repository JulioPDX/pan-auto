interfaces = [
    {
        "virtual_router": "default",
        "zone": "Outside",
        "data": {
            "name": "ethernet1/1",
            "mode": "layer3",
            "link_state": "up",
            "comment": "Outside",
            "enable_dhcp": True,
            "create_dhcp_default_route": True,
        },
    },
    {
        "virtual_router": "default",
        "zone": "DMZ",
        "data": {
            "name": "ethernet1/2",
            "mode": "layer3",
            "link_state": "up",
            "comment": "DMZ",
            "ip": ("10.100.100.1/24"),
        },
    },
    {
        "virtual_router": "default",
        "zone": "Datacenter",
        "data": {
            "name": "ethernet1/3",
            "mode": "layer3",
            "link_state": "up",
            "comment": "Datacenter",
            "ip": ("10.172.20.1/30"),
        },
    },
    {
        "virtual_router": "default",
        "zone": "User LAN",
        "data": {
            "name": "ethernet1/4",
            "mode": "layer3",
            "link_state": "up",
            "comment": "LAN",
            "ip": ("10.17.5.1/30"),
        },
    },
    {
        "virtual_router": "default",
        "zone": "Outside",
        "data": {
            "name": "ethernet1/5",
            "mode": "layer3",
            "link_state": "up",
            "comment": "LAN",
            "ip": ("10.10.10.1/30"),
        },
    },
]
