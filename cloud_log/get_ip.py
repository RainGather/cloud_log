# -*- coding: utf-8 -*-
# Use Success In Python2.7

import socket
import fcntl
import struct
import re

from urllib.request import urlopen


def get_lan_ip():
    ip = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1],
                      [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in
                        [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
    return ip


def get_wan_ip():
    try:
        html = urlopen('http://www.ip.cn/', timeout=5).read().decode('utf-8')
        ip = re.search('\d+\.\d+\.\d+\.\d+', html).group(0)
    except:
        try:
            html = urlopen('http://www.123cha.com/ip/', timeout=5).read().decode('utf-8')
            ip = re.search('\d+\.\d+\.\d+\.\d+', html).group(0)
        except:
            print('Error: Get Wan Ip Error!')
            ip = 'Get Wan Ip Error'
    return ip


if __name__ == '__main__':
    print(get_lan_ip())
    print(get_wan_ip())

