## **Домашнее задание к занятию "5.4. Практические навыки работы с Docker"**
### **Задача 1**
В данном задании вы научитесь изменять существующие Dockerfile, адаптируя их под нужный инфраструктурный стек.

Измените базовый образ предложенного Dockerfile на Arch Linux c сохранением его функциональности.
```
FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:vincent-c/ponysay && \
    apt-get update
 
RUN apt-get install -y ponysay

ENTRYPOINT ["/usr/bin/ponysay"]
CMD ["Hey, netology”]
```
Для получения зачета, вам необходимо предоставить:

* Написанный вами Dockerfile
* Скриншот вывода командной строки после запуска контейнера из вашего базового образа
* Ссылку на образ в вашем хранилище docker-hub

Первый вариант
```
FROM archlinux:latest

RUN useradd -m notroot

RUN pacman -Syy --noconfirm && \
    pacman -Sy --noconfirm git base-devel && \
    pacman -Syu --noconfirm && \
    pacman -Sy --noconfirm ponysay

RUN echo "notroot ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/notroot

USER notroot
WORKDIR /home/notroot

RUN git clone https://aur.archlinux.org/yay-git && \
    cd yay-git && \
    makepkg --noconfirm --syncdeps --rmdeps --install

WORKDIR /pkg
ENTRYPOINT ["/usr/bin/ponysay"]
CMD ["Hey, netology”]
```
Второй вариант
```
FROM archlinux:latest

RUN useradd -m notroot

RUN patched_glibc=glibc-linux4-2.33-4-x86_64.pkg.tar.zst && \
    curl -LO "https://repo.archlinuxcn.org/x86_64/$patched_glibc" && \
    bsdtar -C / -xvf "$patched_glibc"

RUN pacman -Syy --noconfirm && \
    pacman -Sy --noconfirm git base-devel && \
    pacman -Syu --noconfirm && \
    pacman -Sy --noconfirm ponysay

RUN echo "notroot ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/notroot

USER notroot
WORKDIR /home/notroot

RUN git clone https://aur.archlinux.org/yay-git && \
    cd yay-git && \
    makepkg --noconfirm --syncdeps --rmdeps --install

WORKDIR /pkg
ENTRYPOINT ["/usr/bin/ponysay"]
CMD ["Hey, netology”]
```
Собираем образ
```
docker build -t ponysay_arch -f task3_dz1_pony .
```

Запукскаем контейнер
```
docker -it --name pony -P  ponysay_arch
```

Заходим в контейнер 
```
docker run -it  ponysay_arch
```


### **Задача 2**
В данной задаче вы составите несколько разных Dockerfile для проекта Jenkins, опубликуем образ в ```dockerhub.io``` и посмотрим логи этих контейнеров.

> * Составьте 2 Dockerfile:
>> * Общие моменты:
>>> * Образ должен запускать [Jenkins server](https://www.jenkins.io/download/)
>> * Спецификация первого образа:
>>> * Базовый образ - [amazoncorreto](https://hub.docker.com/_/amazoncorretto)
>>> * Присвоить образу тэг ```ver1```
>> * Спецификация второго образа:
>>> * Базовый образ - [ubuntu:latest](https://hub.docker.com/_/ubuntu)
>>> * Присвоить образу тэг ```ver2```
> * Соберите 2 образа по полученным Dockerfile

> * Запустите и проверьте их работоспособность

> * Опубликуйте образы в своём dockerhub.io хранилище

Для получения зачета, вам необходимо предоставить:

* Наполнения 2х Dockerfile из задания
* Скриншоты логов запущенных вами контейнеров (из командной строки)
* Скриншоты веб-интерфейса Jenkins запущенных вами контейнеров (достаточно 1 скриншота на контейнер)
* Ссылки на образы в вашем хранилище docker-hub

### **Создаём докер фаил для Jenkins на Ubuntu  teg ver2**
```
FROM ubuntu:latest

RUN apt-get update && \
    apt install -y openjdk-11-jdk openjdk-11-jre

RUN apt install -y wget gnupg2 git && \
    wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | apt-key add - && \
    sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'

RUN apt-get update && \
    apt-get install -y jenkins

EXPOSE 8080

RUN service jenkins start

ENTRYPOINT ["/bin/bash"]
```
Вторая версия Докерфайла
```
FROM ubuntu:latest

RUN apt-get update && \
    apt install -y openjdk-11-jdk openjdk-11-jre

RUN apt install -y wget gnupg2 git && \
    wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | apt-key add - && \
    sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'

RUN apt-get update && \
    apt-get install -y jenkins

EXPOSE 8080

ENTRYPOINT ["/bin/sh", "-c", "service jenkins start && /bin/bash"]

```
Третья версия Докерфайла
```
FROM ubuntu:latest

RUN apt-get update && \
    apt install -y openjdk-11-jdk openjdk-11-jre

RUN apt install -y wget gnupg2 git && \
    wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | apt-key add - && \
    sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'

RUN apt-get update && \
    apt-get install -y jenkins

EXPOSE 8080

ENTRYPOINT ["/bin/sh", "-c", "/etc/init.d/jenkins start"]

```

Собираем образ для Jenkins на Ubuntu  teg ver2
```
docker build -t ubuntu_jenkins_t_vers2 -f task3_dz2_ubuntu_jenkins .
```

Запускаем докер контейнер
```
docker run -itd --name ubuntu_jenkins -p 8080:8080 ubuntu_jenkins_t_vers2
```

Проверяем наш дженкинс по адресу http://localhost:8080 и если он не доступен то заходим в контейнер
```
docker exec -it ubuntu_jenkins bash

и запускаем дженкинс внутри контейнера коммандой ниже
jenkins start
```

### **Создаём докер фаил для Jenkins на archlinux teg ver1**
```
FROM amazoncorretto

RUN yum update && yum install -y git wget initscripts

RUN wget -O /etc/yum.repos.d/jenkins.repo http://pkg.jenkins.io/redhat-stable/jenkins.repo

RUN rpm --import http://pkg.jenkins.io/redhat-stable/jenkins.io.key

RUN yum update && yum install jenkins -y

EXPOSE 8080

ENTRYPOINT ["/bin/sh", "-c", "/etc/init.d/jenkins start && /bin/bash"]
```
Вторая версия Докерфайла
```
FROM amazoncorretto

RUN yum update && yum install -y git wget initscripts

RUN wget -O /etc/yum.repos.d/jenkins.repo http://pkg.jenkins.io/redhat-stable/jenkins.repo

RUN rpm --import http://pkg.jenkins.io/redhat-stable/jenkins.io.key

RUN yum update && yum install jenkins -y

EXPOSE 8080

ENTRYPOINT ["/bin/sh", "-c", "/etc/init.d/jenkins start"]
```

Собираем образ для Jenkins на amazoncorretto  teg ver1
```
docker build -t amazon_jenkins_t_vers1 -f task3_dz2_amazon_jenkins .
```

Запускаем докер контейнер
```
docker run -itd --name amazon_jenkins -p 8080:8080 amazon_jenkins_t_vers1
```

Проверяем наш дженкинс по адресу http://localhost:8080 и если он не доступен то заходим в контейнер
```
docker exec -it amazon_jenkins bash

и запускаем дженкинс внутри контейнера коммандой ниже
jenkins start
```





### **Задача 3**
В данном задании вы научитесь:

* объединять контейнеры в единую сеть
* исполнять команды "изнутри" контейнера

Для выполнения задания вам нужно:

* Написать Dockerfile:

> * Использовать образ [https://hub.docker.com/_/node](https://hub.docker.com/_/node) как базовый
> * Установить необходимые зависимые библиотеки для запуска npm приложения [https://github.com/simplicitesoftware/nodejs-demo](https://github.com/simplicitesoftware/nodejs-demo)
> * Выставить у приложения (и контейнера) порт 3000 для прослушки входящих запросов
> * Соберите образ и запустите контейнер в фоновом режиме с публикацией порта

* Запустить второй контейнер из образа ubuntu:latest

* Создайть ```docker network``` и добавьте в нее оба запущенных контейнера

* Используя ```docker exec``` запустить командную строку контейнера ```ubuntu``` в интерактивном режиме

* Используя утилиту ```curl``` вызвать путь ```/``` контейнера с npm приложением

Для получения зачета, вам необходимо предоставить:

* Наполнение Dockerfile с npm приложением
* Скриншот вывода вызова команды списка docker сетей (docker network cli)
* Скриншот вызова утилиты curl с успешным ответом

Решение
1) Качаем докер с готовым node js [https://github.com/simplicitesoftware/nodejs-demo](https://github.com/simplicitesoftware/nodejs-demo) 
2) Создаем Dockerfile в скаченной папке 
```
FROM node:lts-alpine3.16

RUN mkdir -p /home/vagrant/node_project && chown -R node:node /home/vagrant/node_project

WORKDIR /home/vagrant/node_project

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 3000

CMD ["node", "app.js"]

```
3) Создаем новый image из Dockerfile с тэгом node0
```
docker build -t node0 -f Dockerfile .
```
4) Запускаем образ ubuntu с именем ubuntu0
```
docker run -itd --name ubuntu0 ubuntu
```
5) Запускае образ node0 под именем node_hw
```
docker run -itd --name node_hw -p 3000:3000 node0
```
6) Создаем новую сеть (по умолчанию сеть dridge) с названием my_network
```
docker network create my_network
```
7) Подсоединяем докер ubuntu0 к созданной сети my_network
```
docker network connect my_network ubuntu0
```
8) Подсоединяем докер node_hw к созданной сети my_network
```
docker network connect my_network node_hw
```
9) Там можено увидеть список сетей
```
docker network ls
```
10) Так можно увидеть список сетей в my_network (можно увидеть что приконектили и какие сети выделены) 
```
docker network inspect my_network
```
11) Заходим в ранее созданный контейнер
```
docker exec -ti ubuntu0 bash
```
12) Из создаданного контейнера ubuntu0 Пингуем проверяем доступность сети 
```
ping -c 3 172.18.1.3
```
13) Из создаданного контейнера ubuntu0 Отправляем curl запрос
```
curl -i http://172.18.0.3:3000
```