
# 1 Задание
'''
a = 1
b = '2'
c = a + int(b)
print(c)
'''
'''
# /home/nevermind/PycharmProjects/pythonProject/devops-netology

import os
from pprint import pprint

input_path = input('Введите путь до локальной директории \n')
bash_command = ["cd " + input_path, 'git status']
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('изменено:') !=-1:
        prepare_result = result.replace('\tизменено:   ', '')
        abs_path = os.path.abspath(prepare_result)
        pprint(abs_path)
        break
'''
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

    # host_obj_list = [{key : value} for key, value in url.items()]
    #
    # with open('hostname.yam', 'w', encoding='utf8') as write_json:
    #     json.dump(host_obj_list, write_json)
    # pprint(f'JSON >>> запись {os.getcwd()}/hostname.json')

Ping_url(url)