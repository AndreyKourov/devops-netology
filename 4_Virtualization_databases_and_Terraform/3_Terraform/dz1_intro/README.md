# Домашнее задание к занятию 1. «Инфраструктура как код»
## Задача 1. Выбор инструментов
### Легенда
Через час совещание, на котором менеджер расскажет о новом проекте. Начать работу над проектом нужно будет уже сегодня. Сейчас известно, что это будет сервис, который ваша компания будет предоставлять внешним заказчикам. Первое время, скорее всего, будет один внешний клиент, со временем внешних клиентов станет больше.

Также по разговорам в компании есть вероятность, что техническое задание ещё не чёткое, что приведёт к большому количеству небольших релизов, тестирований интеграций, откатов, доработок, то есть скучно не будет.

Вам как DevOps-инженеру будет нужно принять решение об инструментах для организации инфраструктуры. В вашей компании уже используются следующие инструменты:

* остатки Сloud Formation,
* некоторые образы сделаны при помощи Packer,
* год назад начали активно использовать Terraform,
* разработчики привыкли использовать Docker,
* уже есть большая база Kubernetes-конфигураций,
* для автоматизации процессов используется Teamcity,
* также есть совсем немного Ansible-скриптов,
* ряд bash-скриптов для упрощения рутинных задач.
На совещании нужно будет выяснить подробности о проекте, чтобы определиться с инструментами:

1) Какой тип инфраструктуры будем использовать для этого проекта: изменяемый или не изменяемый?
2) Будет ли центральный сервер для управления инфраструктурой?
3) Будут ли агенты на серверах?
4) Будут ли использованы средства для управления конфигурацией или инициализации ресурсов?
Так как проект стартует уже сегодня, на совещании нужно будет определиться со всеми этими вопросами.

Вам нужно:
1) Ответить на четыре вопроса из раздела «Легенда».
2) Решить, какие инструменты из уже используемых вы хотели бы применить для нового проекта.
3) Определиться, хотите ли рассмотреть возможность внедрения новых инструментов для этого проекта.
Если для ответов на эти вопросы недостаточно информации, напишите, какие моменты уточните на совещании.

### Ответ
-Какой тип инфраструктуры будем использовать для этого проекта: изменяемый или не изменяемый?  #т.к. у нас уже есть опыт активного использования терраформа, то продолжим его юзать. Значит у нас будет не изменяемая инфраструктура.

-Будет ли центральный сервер для управления инфраструктурой?  #для терраформа не нужен центральный сервер.

-Будут ли агенты на серверах?  #для терраформа агенты не требуются

-Будут ли использованы средства для управления конфигурацией или инициализации ресурсов?  #будем использовать ansible

* Terraform - будет отвечать за инфраструктуру;
* Ansible - будет управлять конфигами;
* Docker - будет крутиться наше приложение. Например сам приклад в одном контейнере, а интеграция на других;
* Kubernetes - будет управлять докер-контейнерами;
* Teamcity - не работал с данным продуктом, но как можно отказаться от "автоматизации процессов";
* Bash - скрипты в кроне без этого никак;

```
Как мы будем получать обновы? Нам нужен Jenkins
Возможно нам нужно подумать о файрволе, т.к. мы полезем на внешку.
```

## Задача 2. Установка терраформ.

[Официальный сайт Terraform](https://www.terraform.io/)

В связи с недоступностью ресурсов для загрузки Terraform на территории РФ вы можете воспользоваться VPN или использовать зеркало YandexCloud:
[ссылки для установки открытого ПО](https://github.com/netology-code/devops-materials/blob/master/README.md)

[Ссылки на зеркало](https://hashicorp-releases.yandexcloud.net/terraform/)

Установите Terraform при помощи менеджера пакетов, используемого в вашей операционной системе. В виде результата этой задачи приложите вывод команды terraform --version.

### Ответ
```
Скачал с зеркала версию terraform_1.1.8
Запустил Vagrant установил в /usr/local/bin/

vagrant@vagrant:/vagrant$ sudo unzip /vagrant/terraform_1.1.8_linux_amd64.zip -d /usr/local/bin/
Archive:  /vagrant/terraform_1.1.8_linux_amd64.zip
  inflating: /usr/local/bin/terraform  
vagrant@vagrant:/vagrant$ terraform --version
Terraform v1.1.8
on linux_amd64

Your version of Terraform is out of date! The latest version
is 1.7.0. You can update by downloading from https://www.terraform.io/downloads.html
vagrant@vagrant:/vagrant$
```

## Задача 3. Поддержка легаси кода.
В какой-то момент вы обновили терраформ до новой версии, например с 0.12 до 0.13. А код одного из проектов настолько устарел, что не может работать с версией 0.13. В связи с этим необходимо сделать так, чтобы вы могли одновременно использовать последнюю версию терраформа установленную при помощи штатного менеджера пакетов и устаревшую версию 0.12.

В виде результата этой задачи приложите вывод --version двух версий терраформа доступных на вашем компьютере или виртуальной машине.

### Ответ
```
Скачал с зеркала версию Скачал с зеркала версию
Создал новую директорию /home/vagrant/terraform_1.7.0 и установил 

vagrant@vagrant:/vagrant$ sudo unzip /vagrant/terraform_1.7.0_linux_amd64.zip -d /home/vagrant/terraform_1.7.0/
Archive:  /vagrant/terraform_1.7.0_linux_amd64.zip
  inflating: /home/vagrant/terraform_1.7.0/terraform  

vagrant@vagrant:~/terraform_1.7.0$ /home/vagrant/terraform_1.7.0/terraform --version
Terraform v1.7.0
on linux_amd64
vagrant@vagrant:~/terraform_1.7.0$
```
