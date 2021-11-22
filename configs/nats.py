nats = [
    {
        "name": "General NAT",
        "description": "General NAT for internet access",
        "nat_type": "ipv4",
        "tag": ["Outside"],
        "fromzone": ["User LAN"],
        "tozone": ["Outside"],
        "to_interface": "ethernet1/1",
        "source": ["All User Subnets"],
        "destination": ["any"],
        "source_translation_type": "dynamic-ip-and-port",
        "source_translation_address_type": "interface-address",
        "source_translation_interface": "ethernet1/1",
        "source_translation_ip_address": None,
        "destination_translated_address": None,
        "service": "any",
    },
]
