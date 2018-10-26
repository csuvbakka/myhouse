import os
import roscraco
import re
import requests
import time

import common.constants as constant
import common.protocol as proto
import common.redis_lib as redis
import common.services as services

from collections import namedtuple


RouterData = namedtuple('RouterData', ['ip', 'model', 'port', 'user', 'password'])


def sanitize_mac_address(mac):
    mac = mac.lower()
    mac = mac.replace('-', '')
    mac = mac.replace(':', '')

    return mac


def ping_address(ip_address, timeout=1):
    if not ip_address:
        return False

    ping_command = 'ping -W %s -c 1 %s > /dev/null' % (
                   str(timeout), ip_address)

    if os.system(ping_command) == 0:
        return True
    else:
        return False


def _router_data():
    with open('/run/secrets/wlan_router') as f:
        ip = f.readline().rstrip()
        model = f.readline().rstrip()
        port = f.readline().rstrip()
        user = f.readline().rstrip()
        password = f.readline().rstrip()
    return RouterData(ip, model, port, user, password)


class DHCP:
    def __init__(self):
        self.redis_connection = redis.create_connection()

        self.mac_regex = re.compile(
            '[0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2}-' +
            '[0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2}')

        self.router_data = _router_data()

        self._controller = roscraco.create_controller(
            roscraco.ROUTER_TP_LINK,
            self.router_data.model,
            self.router_data.ip,
            self.router_data.port,
            self.router_data.user,
            self.router_data.password
        )

    def update(self):
        #connected_wireless_macs = self._get_connected_wireless_macs()
        connected_clients_list = self._controller.get_connected_clients_list()
        for client in connected_clients_list:
            self.redis_connection.rpush(
                    services.wlan_presence,
                    proto.ConnectedDevice(client.client_name, client.ip, client.mac))

    def _get_connected_wireless_macs(self):
        ip = self.router_data.ip
        url = 'http://{}/userRpm/WlanStationRpm.htm'.format(ip)
        referer = 'http://{}'.format(ip)
        page = requests.get(url,
                            auth=(self.router_data.user,
                                  self.router_data.password),
                            headers={'referer': referer})

        macs = self.mac_regex.findall(page.text)
        return [sanitize_mac_address(m) for m in macs]


if __name__ == '__main__':
    dhcp = DHCP()
    while (True):
        dhcp.update()
        time.sleep(30)
