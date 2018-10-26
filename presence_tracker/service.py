import common.constants as constant
import common.protocol as proto
import common.redis_lib as redis
import common.services as services
from common.util import sanitize_mac_address

class Device(object):
    def __init__(self, mac_address, user_name, device_name):
        self.mac_address = mac_address
        self.user_name = user_name
        self.device_name = device_name
        self.status = constant.OFFLINE

def _devices():
    with open('/run/secrets/devices') as f:
        lines = f.readlines()

    devices = []
    for line in lines:
        line = line.strip()
        mac_address, user_name, device_name = line.split(':')
        mac_address = sanitize_mac_address(mac_address)
        devices.append(Device(mac_address, user_name, device_name))
    return devices


class PresenceTracker(object):
    def __init__(self, devices):
        self.devices = devices

    def get_device(self, mac_address):
        for device in self.devices:
            if device.mac_address == mac_address:
                return device

        return None


if __name__ == '__main__':
    redis_connection = redis.create_connection()
    presence_tracker = PresenceTracker(_devices())
    while (True):
        data = redis_connection.blpop(services.wlan_presence, 0)[1]
        updated_device = proto.Device.from_json(data)
        device = presence_tracker.get_device(updated_device.mac)
        if not device:
            continue

        if device.status != updated_device.status:
            redis_connection.rpush(services.presence_tracker, proto.DeviceStatusChange(device.device_name, device.user_name, updated_device.status))

        device.status = updated_device.status
