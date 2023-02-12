## **Домашнее задание к занятию "Языки разметки JSON и YAML"**
### **Цель задания**
В результате выполнения этого задания вы:

1. Познакомитесь с синтаксисами JSON и YAML.
2. Узнаете как преобразовать один формат в другой при помощи пары строк.
### **Чеклист готовности к домашнему заданию**
Установлена библиотека pyyaml для Python 3.

### **Инструкция к заданию**
1. Скопируйте в свой .md-файл содержимое этого файла; исходники можно посмотреть здесь.
2. Заполните недостающие части документа решением задач (заменяйте ???, остальное в шаблоне не меняйте, чтобы не сломать форматирование текста, подсветку синтаксиса и прочее) и отправляйте на проверку. Вместо логов можно вставить скриншоты по желанию.
3. Любые вопросы по выполнению заданий спрашивайте в чате учебной группы и/или в разделе “Вопросы по заданию” в личном кабинете.
### **Дополнительные материалы**
[Полезные ссылки для модуля "Скриптовые языки и языки разметки"](https://github.com/netology-code/sysadm-homeworks/tree/devsys10/04-script-03-yaml/additional-info)

### **Задание 1**
Мы выгрузили JSON, который получили через API запрос к нашему сервису:

    { "info" : "Sample JSON output from our service\t",
        "elements" :[
            { "name" : "first",
            "type" : "server",
            "ip" : 7175 
            }
            { "name" : "second",
            "type" : "proxy",
            "ip : 71.78.22.43
            }
        ]
    }
Нужно найти и исправить все ошибки, которые допускает наш сервис

### **Ваш скрипт:**
    { "info" : "Sample JSON output from our service\t",
        "elements": [
            { 
            "name" : "first",
            "type" : "server",
            "ip" : 7175 
            },
            { 
            "name" : "second",
            "type" : "proxy",
            "ip : 71.78.22.43
            }
        ]
    }
### **Задание 2**
В прошлый рабочий день мы создавали скрипт, позволяющий опрашивать веб-сервисы и получать их IP. К уже реализованному функционалу нам нужно добавить возможность записи JSON и YAML файлов, описывающих наши сервисы. Формат записи JSON по одному сервису: { "имя сервиса" : "его IP"}. Формат записи YAML по одному сервису: - имя сервиса: его IP. Если в момент исполнения скрипта меняется IP у сервиса - он должен так же поменяться в yml и json файле.

### **Ваш скрипт:**
```
#!/usr/bin/env python3

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

```
```

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
```
### **Вывод скрипта при запуске при тестировании:**
```
'URL сервиса drive.google.com, IP сервиса 108.177.119.194'
'URL сервиса mail.google.com, IP сервиса 108.177.126.17'
'URL сервиса google.com, IP сервиса 142.250.153.101'
('[ERROR] URL сервиса drive.google.com IP mismatch: старый IP - 142.251.31.194 '
 'Новый IP - 108.177.119.194')
('[ERROR] URL сервиса mail.google.com IP mismatch: старый IP - 142.251.143.37 '
 'Новый IP - 108.177.126.19')
('[ERROR] URL сервиса google.com IP mismatch: старый IP - 142.250.180.110 '
 'Новый IP - 142.250.153.139')
('JSON >>> запись '
 '/home/nevermind/PycharmProjects/pythonProject/devops-netology/DevOps_and_system_administration/3_Scripting_and_markup_languages:Python,Bash,YAML,JSON/3_JSON_and_YAML_markup_languages/dz/hostname.json')
('JSON >>> запись '
 '/home/nevermind/PycharmProjects/pythonProject/devops-netology/DevOps_and_system_administration/3_Scripting_and_markup_languages:Python,Bash,YAML,JSON/3_JSON_and_YAML_markup_languages/dz/hostname.yaml')

Process finished with exit code 0
```
### **json-файл(ы), который(е) записал ваш скрипт:**
```
[
{"drive.google.com": "108.177.119.194"}, 
{"mail.google.com": "108.177.126.19"}, 
{"google.com": "142.250.153.139"}
]
```
### **yml-файл(ы), который(е) записал ваш скрипт:**
```
- drive.google.com: 108.177.119.194
- mail.google.com: 108.177.126.19
- google.com: 142.250.153.139
```
### **Дополнительное задание (со звездочкой*) - необязательно к выполнению**
Так как команды в нашей компании никак не могут прийти к единому мнению о том, какой формат разметки данных использовать: JSON или YAML, нам нужно реализовать парсер из одного формата в другой. Он должен уметь:

* Принимать на вход имя файла
* Проверять формат исходного файла. Если файл не json или yml - скрипт должен остановить свою работу
* Распознавать какой формат данных в файле. Считается, что файлы *.json и *.yml могут быть перепутаны
* Перекодировать данные из исходного формата во второй доступный (из JSON в YAML, из YAML в JSON)
* При обнаружении ошибки в исходном файле - указать в стандартном выводе строку с ошибкой синтаксиса и её номер
* Полученный файл должен иметь имя исходного файла, разница в наименовании обеспечивается разницей расширения файлов
### **Ваш скрипт:**
    ???
### **Пример работы скрипта:**
    ???

### **Правила приема домашнего задания**
В личном кабинете отправлена ссылка на .md файл в вашем репозитории.

### **Критерии оценки**
Зачет - выполнены все задания, ответы даны в развернутой форме, приложены соответствующие скриншоты и файлы проекта, в выполненных заданиях нет противоречий и нарушения логики.

На доработку - задание выполнено частично или не выполнено, в логике выполнения заданий есть противоречия, существенные недостатки.

Обязательными к выполнению являются задачи без указания звездочки. Их выполнение необходимо для получения зачета и диплома о профессиональной переподготовке. Задачи со звездочкой (*) являются дополнительными задачами и/или задачами повышенной сложности. Они не являются обязательными к выполнению, но помогут вам глубже понять тему.