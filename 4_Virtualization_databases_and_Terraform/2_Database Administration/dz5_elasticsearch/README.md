# Домашнее задание к занятию 5. «Elasticsearch»
## Задача 1
В этом задании вы потренируетесь в:
* установке Elasticsearch,
* первоначальном конфигурировании Elasticsearch,
* запуске Elasticsearch в Docker.

Используя Docker-образ [centos:7](https://hub.docker.com/_/centos) как базовый и [документацию по установке и запуску Elastcisearch:](https://www.elastic.co/guide/en/elasticsearch/reference/current/targz.html)
* составьте Dockerfile-манифест для Elasticsearch,
* соберите Docker-образ и сделайте `push` в ваш docker.io-репозиторий,
* запустите контейнер из получившегося образа и выполните запрос пути `/` c хост-машины.

Требования к `elasticsearch.yml:`
* данные path должны сохраняться в /var/lib,
* имя ноды должно быть netology_test.

В ответе приведите:
* текст Dockerfile-манифеста,
* ссылку на образ в репозитории dockerhub,
* ответ `Elasticsearch` на запрос пути `/` в json-виде.

Подсказки:
* возможно, вам понадобится установка пакета perl-Digest-SHA для корректной работы пакета shasum,
* при сетевых проблемах внимательно изучите кластерные и сетевые настройки в elasticsearch.yml,
* при некоторых проблемах вам поможет Docker-директива ulimit,
* Elasticsearch в логах обычно описывает проблему и пути её решения.

Далее мы будем работать с этим экземпляром Elasticsearch.

### Ответ
1) Сначала ставим Centos
```
root@vagrant:/home/vagrant# docker run centos
root@vagrant:/home/vagrant# docker start centos
root@vagrant:/home/vagrant# docker ps
CONTAINER ID   IMAGE     COMMAND       CREATED      STATUS         PORTS                                       NAMES
d6560fb89a2b   centos    "/bin/bash"   4 days ago   Up 3 seconds   0.0.0.0:8080->8080/tcp, :::8080->8080/tcp   centos
root@vagrant:/home/vagrant# docker exec -it d6560fb89a2b bash

```
2) Ставим wget
```
cd /etc/yum.repos.d/
sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*
sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*
#yum update -y #можно и не обновялять, но желательно
yum install -y wget
```
3) Подключаю vpn ставлю Elastic
```
[root@d6560fb89a2b /]# wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.10.1-linux-x86_64.tar.gz
[root@d6560fb89a2b /]# wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.10.1-linux-x86_64.tar.gz.sha512
[root@d6560fb89a2b /]# shasum -a 512 -c elasticsearch-8.10.1-linux-x86_64.tar.gz.sha512
bash: shasum: command not found
[root@d6560fb89a2b /]# tar -xzf elasticsearch-8.10.1-linux-x86_64.tar.gz
```
4) Согласно ТЗ изменяем имя ноды и изменяем path.data. Кроме этого, отключаем secutity для облегчения работы с контейнером в дальнейшем. В ТЗ не требуется обеспечения шифрования:
```
[root@d6560fb89a2b /]# echo "node.name: netology.test" >> elasticsearch-8.10.1/config/elasticsearch.yml
[root@d6560fb89a2b /]# echo "path.data: /var/lib/elastic" >> elasticsearch-8.10.1/config/elasticsearch.yml
[root@d6560fb89a2b /]# echo "xpack.security.enabled: false" >> elasticsearch-8.10.1/config/elasticsearch.yml
[root@d6560fb89a2b /]# echo "xpack.security.enrollment.enabled: false" >> elasticsearch-8.10.1/config/elasticsearch.yml
[root@d6560fb89a2b /]# echo "xpack.security.http.ssl.enabled: false" >> elasticsearch-8.10.1/config/elasticsearch.yml
[root@d6560fb89a2b /]# echo "xpack.security.transport.ssl.enabled: false" >> elasticsearch-8.10.1/config/elasticsearch.yml
```
5) Создаем пользовтаеля и группу elastcisearch, т.к. из под root elasticsearch не запускается.
```
[root@d6560fb89a2b /]# groupadd elasticsearch
[root@d6560fb89a2b /]# useradd elasticsearch -g elasticsearch -p elasticsearch
[root@d6560fb89a2b /]# mkdir /var/lib/elastic
[root@d6560fb89a2b /]# chown -R elasticsearch:elasticsearch /elasticsearch-8.10.1 /var/lib/elastic
[root@d6560fb89a2b /]# chmod o+x /elasticsearch-8.10.1 /var/lib/elastic
[root@d6560fb89a2b /]# chgrp elasticsearch /elasticsearch-8.10.1 /var/lib/elastic
```
6) Запускаем из под пользователя elasticsearch (для того, чтобы запустить в качестве демона добавляем ключ -d в конце):
```
[root@d6560fb89a2b /]# su - elasticsearch -c "/elasticsearch-8.10.1/bin/elasticsearch -d"
[root@d6560fb89a2b /]# ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.0  12044     8 pts/0    Ss+  Sep18   0:00 /bin/bash
root          15  0.0  0.1  12148  1912 pts/1    Ss   Sep18   0:00 bash
elastic+     171 17.5 63.7 3112224 640596 ?      Sl   17:39   0:53 /elasticsearch-8.10.1/jdk/bin/java -Des.networkaddress.cache.ttl=60 -Des.networkadd
elastic+     191  0.0  0.0 120484   564 ?        Sl   17:39   0:00 /elasticsearch-8.10.1/modules/x-pack-ml/platform/linux-x86_64/bin/controller
root         245  0.0  0.3  44660  3372 pts/1    R+   17:44   0:00 ps aux
```
7) Проверяем
```
[root@d6560fb89a2b /]# curl localhost:9200
{
  "name" : "netology.test",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "eFJHauf1Qa6gbJPIrRw9Mw",
  "version" : {
    "number" : "8.10.1",
    "build_flavor" : "default",
    "build_type" : "tar",
    "build_hash" : "a94744f97522b2b7ee8b5dc13be7ee11082b8d6b",
    "build_date" : "2023-09-14T20:16:27.027355296Z",
    "build_snapshot" : false,
    "lucene_version" : "9.7.0",
    "minimum_wire_compatibility_version" : "7.17.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "You Know, for Search"
}
[root@d6560fb89a2b /]# curl localhost:9200/_cat/shards
[root@d6560fb89a2b /]# curl localhost:9200/_cluster/health
{"cluster_name":"elasticsearch","status":"green","timed_out":false,"number_of_nodes":1,"number_of_data_nodes":1,"active_primary_shards":0,"active_shards":0,"relocating_shards":0,"initializing_shards":0,"unassigned_shards":0,"delayed_unassigned_shards":0,"number_of_pending_tasks":0,"number_of_in_flight_fetch":0,"task_max_waiting_in_queue_millis":0,"active_shards_percent_as_number":100.0}[root@d6560fb89a2b /]# 
```
8) Выходим в vagrant пишим Dockerfile
```
vagrant@server1:~$ cat Dockerfile
FROM centos:latest

RUN cd /etc/yum.repos.d/
RUN sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*
RUN sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*
#RUN yum update -y # не будем обновлять, и так не шибко старое. 
RUN yum install -y wget
RUN wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.10.1-linux-x86_64.tar.gz
RUN tar -xzf elasticsearch-8.10.1-linux-x86_64.tar.gz
RUN echo "node.name: netology.test" >> /elasticsearch-8.10.1/config/elasticsearch.yml
RUN echo "path.data: /var/lib/elastic" >> /elasticsearch-8.10.1/config/elasticsearch.yml
RUN echo "xpack.security.enabled: false" >> /elasticsearch-8.10.1/config/elasticsearch.yml
RUN echo "xpack.security.enrollment.enabled: false" >> /elasticsearch-8.10.1/config/elasticsearch.yml
RUN echo "xpack.security.http.ssl.enabled: false" >> /elasticsearch-8.10.1/config/elasticsearch.yml
RUN echo "xpack.security.transport.ssl.enabled: false" >> /elasticsearch-8.10.1/config/elasticsearch.yml
RUN echo "network.host: 0.0.0.0" >> /elasticsearch-8.10.1/config/elasticsearch.yml # чтобы не только localhost
RUN echo "discovery.type: single-node" >> /elasticsearch-8.10.1/config/elasticsearch.yml # в противном случае не запускается

RUN groupadd elasticsearch
RUN useradd elasticsearch -g elasticsearch -p elasticsearch
RUN mkdir /var/lib/elastic
RUN chown -R elasticsearch:elasticsearch /elasticsearch-8.10.1 /var/lib/elastic
RUN chmod o+x /elasticsearch-8.10.1 /var/lib/elastic
RUN chgrp elasticsearch /elasticsearch-8.10.1 /var/lib/elastic
CMD su - elasticsearch -c /elasticsearch-8.10.1/bin/elasticsearch
```
9) Выполняем сборку
```
root@vagrant:/home/vagrant# DOCKER_BUILDKIT=0 docker build -t dockerhubandrey/elasticsearch_test:1.0 .

root@vagrant:/home/vagrant# docker images
REPOSITORY                           TAG       IMAGE ID       CREATED         SIZE
dockerhubandrey/elasticsearch_test   1.0       eec5798c68ed   6 days ago      3.37GB
```
10) Запускаем
```
root@vagrant:/home/vagrant# docker run -it -p 9200:9200 -d dockerhubandrey/elasticsearch_test:1.0
```
11) Проверяем API запросами
```
root@vagrant:/home/vagrant# curl localhost:9200
{
  "name" : "netology.test",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "RdGnIkdIR8W5qaT0yiEo5g",
  "version" : {
    "number" : "8.10.1",
    "build_flavor" : "default",
    "build_type" : "tar",
    "build_hash" : "a94744f97522b2b7ee8b5dc13be7ee11082b8d6b",
    "build_date" : "2023-09-14T20:16:27.027355296Z",
    "build_snapshot" : false,
    "lucene_version" : "9.7.0",
    "minimum_wire_compatibility_version" : "7.17.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "You Know, for Search"
}

root@vagrant:/home/vagrant# curl -X GET "localhost:9200/_cluster/health?pretty"
{
  "cluster_name" : "elasticsearch",
  "status" : "green",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 0,
  "active_shards" : 0,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 0,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 100.0
}
```
12) Авторизуемся и пушим докер image в свой dockerhub
```
root@vagrant:/home/vagrant# docker login

root@vagrant:/home/vagrant# docker push dockerhubandrey/elasticsearch_test:1.0
```
## Задача 2
В этом задании вы научитесь:
* создавать и удалять индексы
* изучать состояние кластера
* обосновывать причину деградации доступности данных
Ознакомтесь с [документацией](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html) ( [хорошая документация](https://techexpert.tips/ru/elasticsearch-ru/elasticsearch-%D1%81%D0%BE%D0%B7%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5-%D0%B8%D0%BD%D0%B4%D0%B5%D0%BA%D1%81%D0%B0/) ) и добавьте в `elasticsearch` 3 индекса, в соответствии со таблицей:
```
Имя	   Количество реплик	Количество шард
ind-1	   0	                1
ind-2	   1                	2
ind-3	   2	                4
```
Получите список индексов и их статусов, используя API и **приведите в ответе** на задание.

Получите состояние кластера `elasticsearch`, используя API.

Как вы думаете, почему часть индексов и кластер находится в состоянии yellow?

Удалите все индексы.

**Важно**

При проектировании кластера elasticsearch нужно корректно рассчитывать количество реплик и шард, иначе возможна потеря данных индексов, вплоть до полной, при деградации системы.

### Ответ
1) Создаем 3 индекса ind-1, ind-2, ind-3:
```
root@vagrant:/home/vagrant# curl -X PUT "localhost:9200/ind-1?pretty" -H 'Content-Type: application/json' -d'{"settings": {"index": {"number_of_shards": 1,  "number_of_replicas": 0 }}}'
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "ind-1"
}
root@vagrant:/home/vagrant# curl -X PUT "localhost:9200/ind-2?pretty" -H 'Content-Type: application/json' -d'{"settings": {"index": {"number_of_shards": 2,  "number_of_replicas": 1 }}}'
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "ind-2"
}
root@vagrant:/home/vagrant# curl -X PUT "localhost:9200/ind-3?pretty" -H 'Content-Type: application/json' -d'{"settings": {"index": {"number_of_shards": 4,  "number_of_replicas": 2 }}}'
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "ind-3"
}
```
2) Проверяем
```
root@vagrant:/home/vagrant# curl -X GET "localhost:9200/ind-1,ind-2,ind-3?pretty"
{
  "ind-1" : {
    "aliases" : { },
    "mappings" : { },
    "settings" : {
      "index" : {
        "routing" : {
          "allocation" : {
            "include" : {
              "_tier_preference" : "data_content"
            }
          }
        },
        "number_of_shards" : "1",
        "provided_name" : "ind-1",
        "creation_date" : "1696523678158",
        "number_of_replicas" : "0",
        "uuid" : "EvwWrZJHQ3-4n1eMkXo8gg",
        "version" : {
          "created" : "8100199"
        }
      }
    }
  },
  "ind-2" : {
    "aliases" : { },
    "mappings" : { },
    "settings" : {
      "index" : {
        "routing" : {
          "allocation" : {
            "include" : {
              "_tier_preference" : "data_content"
            }
          }
        },
        "number_of_shards" : "2",
        "provided_name" : "ind-2",
        "creation_date" : "1696523700124",
        "number_of_replicas" : "1",
        "uuid" : "E-OcelnbR2qEuu_NSvmirQ",
        "version" : {
          "created" : "8100199"
        }
      }
    }
  },
  "ind-3" : {
    "aliases" : { },
    "mappings" : { },
    "settings" : {
      "index" : {
        "routing" : {
          "allocation" : {
            "include" : {
              "_tier_preference" : "data_content"
            }
          }
        },
        "number_of_shards" : "4",
        "provided_name" : "ind-3",
        "creation_date" : "1696523720589",
        "number_of_replicas" : "2",
        "uuid" : "hvt13_MhQqerfKDY2RElJw",
        "version" : {
          "created" : "8100199"
        }
      }
    }
  }
}
root@vagrant:/home/vagrant#
```
3) Проверяем состояние кластера. Состояние кластера "YELLOW" в связи с тем, что необходимы дополнительные ноды для создаения реплик, которые мы затребовали при создаении индексов. Соответсвенно для GREEN статус требуется добавить дополнительно 2 ноды при сохранении кол-ва реплик у ind-3.
```
root@vagrant:/home/vagrant# curl -X GET "localhost:9200/_cluster/health?pretty"
{
  "cluster_name" : "elasticsearch",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 7,
  "active_shards" : 7,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 10,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 41.17647058823529
}
root@vagrant:/home/vagrant# 
```
4) Удаляем все индексы
```
root@vagrant:/home/vagrant# curl -X DELETE "localhost:9200/ind-1,ind-2,ind-3?pretty"
{
  "acknowledged" : true
}
root@vagrant:/home/vagrant#
```
5) Проверяем что индексы удалилсь
```
root@vagrant:/home/vagrant# curl -X GET "localhost:9200/ind-1,ind-2,ind-3?pretty"
{
  "error" : {
    "root_cause" : [
      {
        "type" : "index_not_found_exception",
        "reason" : "no such index [ind-1]",
        "resource.type" : "index_or_alias",
        "resource.id" : "ind-1",
        "index_uuid" : "_na_",
        "index" : "ind-1"
      }
    ],
    "type" : "index_not_found_exception",
    "reason" : "no such index [ind-1]",
    "resource.type" : "index_or_alias",
    "resource.id" : "ind-1",
    "index_uuid" : "_na_",
    "index" : "ind-1"
  },
  "status" : 404
}
root@vagrant:/home/vagrant#
```
## Задача 3
В данном задании вы научитесь:
* создавать бэкапы данных
* восстанавливать индексы из бэкапов

Создайте директорию `{путь до корневой директории с elasticsearch в образе}/snapshots`.

Используя API [зарегистрируйте](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-register-repository.html#snapshots-register-repository) данную директорию как `snapshot repository` c именем `netology_backup`.

**Приведите в ответе** запрос API и результат вызова API для создания репозитория.

Создайте индекс `test` с 0 реплик и 1 шардом и **приведите в ответе** список индексов.

[Создайте snapshot](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-take-snapshot.html) состояния кластера `elasticsearch`.

**Приведите в ответе** список файлов в директории со `snapshot`ами.

Удалите индекс `test` и создайте индекс `test-2`. **Приведите в ответе** список индексов.

[Восстановите](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-restore-snapshot.html) состояние кластера `elasticsearch` из `snapshot`, созданного ранее.

**Приведите в ответе** запрос к API восстановления и итоговый список индексов.

Подсказки:

* возможно вам понадобится доработать `elasticsearch.yml` в части директивы `path.repo` и перезапустить `elasticsearch`

### Ответ
1) Создаем директорию snapshot, назначем права для пользователя elasticsearch, добавляем настройки репозитория и рестартуем контейнер.
```
[root@a95f1d995e24 /]# mkdir /elasticsearch-8.10.1/snapshots
[root@a95f1d995e24 /]# chown elasticsearch:elasticsearch /elasticsearch-8.10.1/snapshots
[root@a95f1d995e24 /]# echo "path.repo: /elasticsearch-8.10.1/snapshots >> /elasticsearch-8.10.1/config/elasticsearch.yml
[root@a95f1d995e24 /]# exit

root@vagrant:/home/vagrant# docker ps
CONTAINER ID   IMAGE                                    COMMAND                  CREATED      STATUS      PORTS                                       NAMES
a95f1d995e24   dockerhubandrey/elasticsearch_test:1.0   "/bin/sh -c 'su - el…"   3 days ago   Up 3 days   0.0.0.0:9200->9200/tcp, :::9200->9200/tcp   confident_gagarin
root@vagrant:/home/vagrant# docker restart a95f1d995e24
```
2) Регистрируем директорию, как netology_backup через API и проверяем
```
root@vagrant:/home/vagrant# curl -X PUT "localhost:9200/_snapshot/netology_backup?pretty" -H 'Content-Type: application/json' -d'{"type": "fs","settings": {"location": "/elasticsearch-8.10.1/snapshots"}}'
{
  "acknowledged" : true
}
root@vagrant:/home/vagrant# curl -X POST "localhost:9200/_snapshot/netology_backup/_verify?pretty"
{
  "nodes" : {
    "ktD3CufnTs2BYrf_AorMPg" : {
      "name" : "netology.test"
    }
  }
}
root@vagrant:/home/vagrant#
```
3) Добавляем индекс test согласно задания и проверяем
```
root@vagrant:/home/vagrant# curl -X PUT "localhost:9200/test?pretty" -H 'Content-Type: application/json' -d'{"settings": {"index": {"number_of_shards": 1,  "number_of_replicas": 0 }}}'
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "test"
}
root@vagrant:/home/vagrant# curl -X GET "localhost:9200/_cat/indices?v=true"
health status index uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   test  E3LAdS8hSHuTe4WT2UqmSA   1   0          0            0       226b           226b
root@vagrant:/home/vagrant#
```
4) Делаем бекап в netology_backup (добавили ?wait_for_completion=true для визуального понимания завершения) и делаем проверку
```
root@vagrant:/home/vagrant# curl -X PUT "localhost:9200/_snapshot/netology_backup/my_snapshot?wait_for_completion=true&pretty"
{
  "snapshot" : {
    "snapshot" : "my_snapshot",
    "uuid" : "CABV58ETT4aRMmu4uw1Gpw",
    "repository" : "netology_backup",
    "version_id" : 8100199,
    "version" : "8100199",
    "indices" : [
      "test"
    ],
    "data_streams" : [ ],
    "include_global_state" : true,
    "state" : "SUCCESS",
    "start_time" : "2023-10-09T15:05:30.878Z",
    "start_time_in_millis" : 1696863930878,
    "end_time" : "2023-10-09T15:05:30.878Z",
    "end_time_in_millis" : 1696863930878,
    "duration_in_millis" : 0,
    "failures" : [ ],
    "shards" : {
      "total" : 1,
      "failed" : 0,
      "successful" : 1
    },
    "feature_states" : [ ]
  }
}
root@vagrant:/home/vagrant# curl -X GET "localhost:9200/_snapshot?pretty"
{
  "netology_backup" : {
    "type" : "fs",
    "uuid" : "BmraSe5PTwaE1tc2HJ7LSQ",
    "settings" : {
      "location" : "/elasticsearch-8.10.1/snapshots"
    }
  }
}
root@vagrant:/home/vagrant# curl -X GET "localhost:9200/_snapshot/netology_backup/*?verbose=false&pretty"
{
  "snapshots" : [
    {
      "snapshot" : "my_snapshot",
      "uuid" : "CABV58ETT4aRMmu4uw1Gpw",
      "repository" : "netology_backup",
      "indices" : [
        "test"
      ],
      "data_streams" : [ ],
      "state" : "SUCCESS"
    }
  ],
  "total" : 1,
  "remaining" : 0
}
root@vagrant:/home/vagrant#
```
5) Проверяем директорию /elasticsearch-8.10.1/snapshots/ внутри контейнера
```
root@vagrant:/home/vagrant# docker exec -it a95f1d995e24 bash

[root@a95f1d995e24 /]# ls -la elasticsearch-8.10.1/snapshots/
total 52
drwxr-xr-x 3 elasticsearch elasticsearch  4096 Oct  9 15:05 .
drwxr-xr-x 1 elasticsearch elasticsearch  4096 Oct  8 17:01 ..
-rw-rw-r-- 1 elasticsearch elasticsearch   587 Oct  9 15:05 index-0
-rw-rw-r-- 1 elasticsearch elasticsearch     8 Oct  9 15:05 index.latest
drwxrwxr-x 3 elasticsearch elasticsearch  4096 Oct  9 15:05 indices
-rw-rw-r-- 1 elasticsearch elasticsearch 23685 Oct  9 15:05 meta-CABV58ETT4aRMmu4uw1Gpw.dat
-rw-rw-r-- 1 elasticsearch elasticsearch   304 Oct  9 15:05 snap-CABV58ETT4aRMmu4uw1Gpw.dat
[root@a95f1d995e24 /]#
```
6) Удаляем индекс test
```
[root@a95f1d995e24 /]# curl -X DELETE "localhost:9200/test?pretty"
{
  "acknowledged" : true
}
[root@a95f1d995e24 /]#
```
7) Создаем индекс test-2 и проверяем список
```
root@vagrant:/home/vagrant# curl -X PUT "localhost:9200/test-2?pretty" -H 'Content-Type: application/json' -d'{"settings": {"index": {"number_of_shards": 1,  "number_of_replicas": 0 }}}'
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "test-2"
}
root@vagrant:/home/vagrant# curl -X GET "localhost:9200/_cat/indices?v=true"
health status index  uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   test-2 fK9Hd__9TNOL-pwf4COlQw   1   0          0            0       226b           226b
root@vagrant:/home/vagrant# 
```
8) Выполняем восстанавление из бекапа
```
root@vagrant:/home/vagrant# curl -X POST "localhost:9200/_snapshot/netology_backup/my_snapshot/_restore?pretty" -H 'Content-Type: application/json' -d' { "indices": "*", "include_global_state": true } '
{
  "accepted" : true
}
root@vagrant:/home/vagrant# 
```
9) Проверяем список индексов и видем два индекса. Один созданный test-2 и восстановленный из бекапа
```
root@vagrant:/home/vagrant# curl -X GET "localhost:9200/_cat/indices?v=true"
health status index  uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   test-2 fK9Hd__9TNOL-pwf4COlQw   1   0          0            0       248b           248b
green  open   test   RL15gTa7TxiZP6WOuQWGew   1   0          0            0       248b           248b
root@vagrant:/home/vagrant# 
```