address_groups = [
    {
        "name": "IT Users",
        "static_value": ["IT Administrators", "IT Developers"],
        "tag": "User LAN",
    },
    {
        "name": "Operations User Subnets",
        "static_value": ["Operations-Finance", "Operations-Sales"],
        "tag": "User LAN",
    },
    {
        "name": "Datacenter Subnets",
        "static_value": [
            "Datacenter Applications",
            "Datacenter Infrastructure",
            "Datacenter Internal DNS",
            "Some Test",
        ],
        "tag": "Datacenter",
    },
    {
        "name": "All User Subnets",
        "static_value": ["IT Users", "Operations User Subnets"],
        "tag": "User LAN",
    },
]
