def sanitize_mac_address(mac):
    mac = mac.lower()
    mac = mac.replace('-', '')
    mac = mac.replace(':', '')

    return mac
