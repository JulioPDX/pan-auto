zones = [
    {
        "name": "User LAN",
        "mode": "layer3",
        "zone_profile": "DefaultZoneProtectionProfile",
        "log_setting": "Zone-Forwarding-Profile",
        "enable_packet_buffer_protection": True,
    },
    {
        "name": "Datacenter",
        "mode": "layer3",
        "zone_profile": "DefaultZoneProtectionProfile",
        "log_setting": "Zone-Forwarding-Profile",
        "enable_packet_buffer_protection": True,
    },
    {
        "name": "DMZ",
        "mode": "layer3",
        "zone_profile": "DefaultZoneProtectionProfile",
        "log_setting": "Zone-Forwarding-Profile",
        "enable_packet_buffer_protection": True,
    },
    {
        "name": "Outside",
        "mode": "layer3",
        "zone_profile": "OutsideZoneProtectionProfile",
        "log_setting": "Zone-Forwarding-Profile",
        "enable_packet_buffer_protection": True,
    },
    {
        "name": "Test",
        "mode": "layer3",
        "zone_profile": "OutsideZoneProtectionProfile",
        "log_setting": "Zone-Forwarding-Profile",
        "enable_packet_buffer_protection": True,
    },
]
