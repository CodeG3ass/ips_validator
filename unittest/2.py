import unittest
from test import *
import re
import ipaddress

class TestMyFunction(unittest.TestCase):
    def test_ip_range(self):
        # Тестирование диапазона IP-адресов
        line = "192.168.88.0-192.168.88.255"
        ip_addresses = set()
        ip_range = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}-\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', line)
        if ip_range:
            start_ip, end_ip = ip_range.group().split('-')
            start_ip = ipaddress.ip_address(start_ip)
            end_ip = ipaddress.ip_address(end_ip)
            for ip in range(int(start_ip), int(end_ip) + 1):
                ip_addresses.add(str(ipaddress.ip_address(ip)))
                print(str(ipaddress.ip_address(ip)))
        self.assertEqual(len(ip_addresses), 256)

    def test_single_ip(self):
        # Тестирование одного IP-адреса
        line = "192.168.88.1/24"
        ip_addresses = set()
        ip_address = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?:\/[0-9]{1,2})?\b', line)
        if ip_address:
            ip_network = ipaddress.ip_network(ip_address.group(), strict=False)
            for ip in ip_network.hosts():
                ip_addresses.add(str(ip))
        self.assertEqual(len(ip_addresses), 254)

if __name__ == '__main__':
    unittest.main()
