#!/usr/bin/env python3
'''
'''
# Вариант 1
import socket
import os
import json
import yaml

hostnames = {'drive.google.com': '64.233.164.194', 'mail.google.com': '64.233.165.19', 'google.com': '64.233.165.113'}

for hostname, value in hostnames.items():
    try:
        ip = socket.gethostbyname(hostname)
        #print(f'The {hostname} IP Address is {ip}')
        if value == ip:
            print(f'{hostname}: IP {value} в словаре и последний полученный {ip} СОВПАДАЮТ, все ок не трогаем')
        else:
            print(f'{hostname}:  IP {value} в словаре и последний полученный {ip} НЕ_СОВПАДАЮТ, надо апдейтить')
            hostnames[hostname] = ip
    except socket.gaierror as e:
        hostnames[hostname] = None
        print(f'[ERROR] {hostname} не резолвится {e}')
print(f'DICT update >>> {hostnames}')

host_obj_list = [{hostname: value} for hostname, value in hostnames.items()]

with open('hostnames.json', 'w', encoding='utf8') as write_json2:
    json.dump(host_obj_list, write_json2)
print(f'JSON >>> записали сюда {os.getcwd()}/hostnames.json')

with open('hostnames.yml', 'w', encoding='utf8') as write_yaml2:
    yaml.dump(host_obj_list, write_yaml2, default_flow_style=False, allow_unicode=True)
print(f'YAML >>> записали сюда {os.getcwd()}/hostnames.yml')


# Вариант 2
import os
from pprint import pprint
import socket
import yaml
import json

url = {'drive.google.com' : '142.251.31.194', 'mail.google.com': '142.251.143.37', 'google.com': '142.250.180.110'}

class Ping_url():
    def __init__(self, url):
        self.url = url
    new_url = {}
    for k, v in url.items():
        apdt_url = socket.gethostbyname(k)
        pprint(f'URL сервиса {k}, IP сервиса {apdt_url}')
    for key, value in url.items():
        socket_url = socket.gethostbyname(key)
        if value == socket_url:
            pprint(f'URL сервиса {key} его ip {value}')
        else:
            pprint(f'[ERROR] URL сервиса {key} IP mismatch: старый IP - {value} Новый IP - {socket_url}')
            url[key] = socket_url

    host_obj_list = [{key : value} for key, value in url.items()]

    with open('hostname.json', 'w', encoding='utf8') as write_json:
        json.dump(host_obj_list, write_json)
    pprint(f'JSON >>> запись {os.getcwd()}/hostname.json')

    with open('hostname.yam', 'w', encoding='utf8') as write_yaml:
        yaml.dump(host_obj_list, write_yaml)
    pprint(f'JSON >>> запись {os.getcwd()}/hostname.yaml')

Ping_url(url)