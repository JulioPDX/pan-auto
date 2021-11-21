routing = [
    {
        "virtual_router": "default",
        "ospf": {
            "data": {
                "enable": True,
                "reject_default_route": True,
                "router_id": "10.17.5.1",
                "allow_redist_default_route": True,
            },
            "redis_profiles": [
                {
                    "data": {
                        "name": "DefaultRoute",
                        "priority": 1,
                        "filter_type": ("static"),
                        "action": "redist",
                    },
                    "ospf_export_rules": [
                        {"name": "DefaultRoute", "new_path_type": "ext-2"}
                    ],
                },
            ],
            "areas": [
                {
                    "data": {
                        "name": "0.0.0.0",
                        "type": "normal",
                    },
                    "ranges": [
                        {
                            "name": "192.168.10.0/24",
                            "mode": "advertise",
                        },
                        {
                            "name": "10.100.100.0/24",
                            "mode": "advertise",
                        },
                        {
                            "name": "10.172.20.0/30",
                            "mode": "advertise",
                        },
                        {
                            "name": "10.17.5.0/30",
                            "mode": "advertise",
                        },
                    ],
                    "interfaces": [
                        {
                            "name": "ethernet1/2",
                            "enable": True,
                            "link_type": "p2p",
                            "passive": True,
                        },
                        {
                            "name": "ethernet1/3",
                            "enable": True,
                            "link_type": "broadcast",
                            "passive": False,
                        },
                        {
                            "name": "ethernet1/4",
                            "enable": True,
                            "link_type": "broadcast",
                            "passive": False,
                        },
                    ],
                }
            ],
        },
    }
]
