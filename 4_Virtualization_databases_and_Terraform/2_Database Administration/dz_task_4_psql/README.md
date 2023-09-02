# Домашнее задание к занятию "6.4. PostgreSQL"

## Задача 1

Используя docker поднимите инстанс PostgreSQL (версию 13). Данные БД сохраните в volume.
Подключитесь к БД PostgreSQL используя `psql`.
Воспользуйтесь командой `\?` для вывода подсказки по имеющимся в `psql` управляющим командам.

**Найдите и приведите** управляющие команды для:
- вывода списка БД
- подключения к БД
- вывода списка таблиц
- вывода описания содержимого таблиц
- выхода из psql

### Ответ

Создаем контейнер postgres:latest (ошибочно выбран latest, т.к. предполагалась версия 13).

```
1) Содаем 
root@vagrant:/home/vagrant# docker run --name pgdb -p 5432:5432 -v /vagrant/data1:/mnt/data1 -e POSTGRES_PASSWORD=password -d postgres:latest

2) Подключаемся
root@vagrant:/home/vagrant# docker exec -it pgdb  bash

3) Вывод списка БД
postgres=# \l[+]   [PATTERN]      list databases

4) Подключения к БД
postgres=# \c[onnect] {[DBNAME|- USER|- HOST|- PORT|-] | conninfo}
                         connect to new database (currently "postgres")

5) Вывод списка таблиц
postgres=# \d[S+]                 list tables, views, and sequences
           \dt[S+] [PATTERN]      list tables

6) Вывод описания содержимого таблиц
postgres=# \d[S+]  NAME           describe table, view, sequence, or index

7) Выход из psql
postgres=# \q                     quit psql
```

## Задача 2
* Используя `psql` создайте БД test_database. 
* [Изучите бэкап БД](https://github.com/netology-code/virt-homeworks/tree/master/06-db-04-postgresql/test_data).
* Восстановите бэкап БД в `test_database`. 
* Перейдите в управляющую консоль `psql` внутри контейнера. 
* Подключитесь к восстановленной БД и проведите операцию ANALYZE для сбора статистики по таблице. 
* Используя таблицу [pg_stats](https://postgrespro.ru/docs/postgresql/12/view-pg-stats), найдите столбец таблицы `orders` с наибольшим средним значением размера 
элементов в байтах. 
* Приведите в ответе команду, которую вы использовали для вычисления и полученный 
результат.

### Ответ
```
1) Подключаемся к докер образу
root@vagrant:/home/vagrant# docker exec -it pgdb  bash

2) Подключаемся из Docker образа к psql
root@f678ece9afb4:/mnt# psql --username=postgres

3) Создаем БД test_database
postgres=# CREATE DATABASE test_database;

4) Выходим из psql обратно в докер образ
postgres=# \q

5) Восстанавливаем таблицу из дампа:
    ПЕРВЫЙ Способ ( ИЗ ВАГРАНТА )
root@vagrant:/home/vagrant# psql -h localhost -p 5432 --username=postgres  test_database < /mnt/data1/test_dump.sql

    ВТОРОЙ Способ ( ИЗ ДОКЕР ОБРАЗА )
root@f678ece9afb4:/mnt# psql --username=postgres -d test_database -f /mnt/data1/test_dump.sql

6) Находясь в psql подключаемся к БД test_database
postgres=# \c test_database

7) Смотрим таблицы в БД test_database
test_database=# \dt+
                                      List of relations
 Schema |  Name  | Type  |  Owner   | Persistence | Access method |    Size    | Description 
--------+--------+-------+----------+-------------+---------------+------------+-------------
 public | orders | table | postgres | permanent   | heap          | 8192 bytes | 
(1 row)

8) Проверяем SELECT
test_database=# SELECT * from orders;
 id |        title         | price 
----+----------------------+-------
  1 | War and peace        |   100
  2 | My little database   |   500
  3 | Adventure psql time  |   300
  4 | Server gravity falls |   300
  5 | Log gossips          |   123
  6 | WAL never lies       |   900
  7 | Me and my bash-pet   |   499
  8 | Dbiezdmin            |   501
(8 rows)

9) Выполняем тест с помощью ANALYZE согласно заданию
test_database=# ANALYZE VERBOSE orders;
INFO:  analyzing "public.orders"
INFO:  "orders": scanned 1 of 1 pages, containing 8 live rows and 0 dead rows; 8 rows in sample, 8 estimated total rows
ANALYZE

10) Выполняем поиск максимального столбца в байтах в таблице orders 
    ПЕРВЫЙ способ
test_database=#  
SELECT tablename, attname ,avg_width FROM pg_stats WHERE tablename = 'orders';
 tablename | attname | avg_width 
-----------+---------+-----------
 orders    | id      |         4
 orders    | title   |        16
 orders    | price   |         4
(3 rows)

test_database=#  
SELECT tablename, attname , avg_width FROM pg_stats WHERE tablename = 'orders' ORDER BY avg_width DESC LIMIT 1;
 tablename | attname | avg_width 
-----------+---------+-----------
 orders    | title   |        16
(1 row)

    ВТОРОЙ способ
test_database=#                  
SELECT tablename, attname , avg_width FROM pg_stats WHERE tablename = 'orders' AND avg_width = (SELECT MAX(avg_width) from pg_stats WHERE tablename = 'orders');
 tablename | attname | avg_width 
-----------+---------+-----------
 orders    | title   |        16
(1 row)        

    ТРЕТИЙ способ
test_database=# SELECT attname, avg_width FROM pg_stats WHERE avg_width = (SELECT max(avg_width) FROM pg_stats);
  attname   | avg_width 
------------+-----------
 prosqlbody |      1278
(1 row)
   
```

## Задача 3
Архитектор и администратор БД выяснили, что ваша таблица orders разрослась до невиданных размеров и поиск по ней занимает долгое время. Вам как успешному выпускнику курсов DevOps в Нетологии предложили провести разбиение таблицы на 2: шардировать на orders_1 - price>499 и orders_2 - price<=499.
* Предложите SQL-транзакцию для проведения этой операции.
* Можно ли было изначально исключить ручное разбиение при проектировании таблицы orders?

### Ответ
1) Внутри БД test_database оздаем таблицы orders_1 и orders_2 для шардинга:
```
test_database=# CREATE TABLE orders_1 ( CHECK (price > 499)) INHERITS (orders);
CREATE TABLE
test_database=# CREATE TABLE orders_2 ( CHECK (price <= 499)) INHERITS (orders);
CREATE TABLE

test_database=# SELECT * FROM orders_1;
 id | title | price 
----+-------+-------
(0 rows)

test_database=# SELECT * FROM orders_2;
 id | title | price 
----+-------+-------
(0 rows)
```
2) Наполняем таблицу данными из основной таблицы и очищаем таблицу orders (не забываем поставить параметр ONLY, иначе очистятся таблицы шардинга):
```
INSERT INTO orders_1 (id, title, price) SELECT id, title, price FROM orders WHERE price > 499;
INSERT INTO orders_2 (id, title, price) SELECT id, title, price FROM orders WHERE price <= 499;
DELETE FROM ONLY orders;
```
3) Создаем правила для автоматического шардирования по условиям из задания (для исклюяения ручного разбиения):
```
test_database=# CREATE RULE orders_insert_to_1 AS ON INSERT TO orders WHERE (price > 499) DO INSTEAD INSERT INTO orders_1 VALUES (NEW.*);
CREATE RULE
test_database=# CREATE RULE orders_insert_to_2 AS ON INSERT TO orders WHERE (price <= 499) DO INSTEAD INSERT INTO orders_2 VALUES (NEW.*);
CREATE RULE
```
4) Проверяем работоспособность правил (предварительно очищая таблицу orders и все ее шардинг таблицы):
```
test_database=# DELETE FROM orders;

test_database=# SELECT * FROM ONLY orders;
 id | title | price 
----+-------+-------
(0 rows)

test_database=# INSERT INTO orders (id, title, price) VALUES (1,'War and peace', 100);
test_database=# INSERT INTO orders (id, title, price) VALUES (2,'My little database', 500);
test_database=# INSERT INTO orders (id, title, price) VALUES (3,'Adventure psql time', 300);
test_database=# INSERT INTO orders (id, title, price) VALUES (4,'Server gravity falls', 300);
test_database=# INSERT INTO orders (id, title, price) VALUES (5,'Log gossips', 123);
test_database=# INSERT INTO orders (id, title, price) VALUES (6,'WAL never lies', 900);
test_database=# INSERT INTO orders (id, title, price) VALUES (7,'Me and my bash-pet', 499);
test_database=# INSERT INTO orders (id, title, price) VALUES (8,'Dbiezdmin', 501);

test_database=# SELECT * FROM  orders;
 id |        title         | price 
----+----------------------+-------
  2 | My little database   |   500
  6 | WAL never lies       |   900
  8 | Dbiezdmin            |   501
  1 | War and peace        |   100
  3 | Adventure psql time  |   300
  4 | Server gravity falls |   300
  5 | Log gossips          |   123
  7 | Me and my bash-pet   |   499
(8 rows)

test_database=# SELECT * FROM orders_1;
 id |       title        | price 
----+--------------------+-------
  2 | My little database |   500
  6 | WAL never lies     |   900
  8 | Dbiezdmin          |   501
(3 rows)

test_database=# SELECT * FROM orders_2;
 id |        title         | price 
----+----------------------+-------
  1 | War and peace        |   100
  3 | Adventure psql time  |   300
  4 | Server gravity falls |   300
  5 | Log gossips          |   123
  7 | Me and my bash-pet   |   499
(5 rows)
```
## Задача 4

* Используя утилиту `pg_dump` создайте бекап БД `test_database`. 
* Как бы вы доработали бэкап-файл, чтобы добавить уникальность значения столбца `title` для таблиц `test_database`?

### Ответ
Выполняем backup таблиц БД test_database в файл test_database_shard.backup:

```
root@vagrant:/home/vagrant# docker exec -it f678ece9afb4 pg_dump -U postgres -f /mnt/data1/test_database_shard.backup test_database

Проверяем наличие файла

root@vagrant:/home/vagrant# ll /vagrant/data1/
total 16
drwxrwxr-x 1 vagrant vagrant 4096 Sep  2 07:36 ./
drwxrwxr-x 1 vagrant vagrant 4096 Aug 11 17:01 ../
-rw-r--r-- 1 vagrant vagrant 4066 Sep  2 07:36 test_database_shard.backup
-rw-rw-r-- 1 vagrant vagrant 2082 Aug 26 18:40 test_dump.sql

```

Смотрим вывод файла

```
root@vagrant:/home/vagrant# cat /vagrant/data1/test_database_shard.backup 
--
-- PostgreSQL database dump
--

-- Dumped from database version 15.3 (Debian 15.3-1.pgdg120+1)
-- Dumped by pg_dump version 15.3 (Debian 15.3-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    id integer NOT NULL,
    title character varying(80) NOT NULL,
    price integer DEFAULT 0
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- Name: orders_1; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders_1 (
    CONSTRAINT orders_1_price_check CHECK ((price > 499))
)
INHERITS (public.orders);


ALTER TABLE public.orders_1 OWNER TO postgres;

--
-- Name: orders_2; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders_2 (
    CONSTRAINT orders_2_price_check CHECK ((price <= 499))
)
INHERITS (public.orders);


ALTER TABLE public.orders_2 OWNER TO postgres;

--
-- Name: orders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.orders_id_seq OWNER TO postgres;

--
-- Name: orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;


--
-- Name: orders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- Name: orders_1 id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders_1 ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- Name: orders_1 price; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders_1 ALTER COLUMN price SET DEFAULT 0;


--
-- Name: orders_2 id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders_2 ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- Name: orders_2 price; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders_2 ALTER COLUMN price SET DEFAULT 0;


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders (id, title, price) FROM stdin;
\.


--
-- Data for Name: orders_1; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders_1 (id, title, price) FROM stdin;
2	My little database	500
6	WAL never lies	900
8	Dbiezdmin	501
\.


--
-- Data for Name: orders_2; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders_2 (id, title, price) FROM stdin;
1	War and peace	100
3	Adventure psql time	300
4	Server gravity falls	300
5	Log gossips	123
7	Me and my bash-pet	499
\.


--
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orders_id_seq', 8, true);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- Name: orders orders_insert_to_1; Type: RULE; Schema: public; Owner: postgres
--

CREATE RULE orders_insert_to_1 AS
    ON INSERT TO public.orders
   WHERE (new.price > 499) DO INSTEAD  INSERT INTO public.orders_1 (id, title, price)
  VALUES (new.id, new.title, new.price);


--
-- Name: orders orders_insert_to_2; Type: RULE; Schema: public; Owner: postgres
--

CREATE RULE orders_insert_to_2 AS
    ON INSERT TO public.orders
   WHERE (new.price <= 499) DO INSTEAD  INSERT INTO public.orders_2 (id, title, price)
  VALUES (new.id, new.title, new.price);


--
-- PostgreSQL database dump complete
--

root@vagrant:/home/vagrant#

```

Для того, чтобы добавить уникальность поля title можно добавить уникальное ограничение в бекап, а именно:

```
ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);
+   ADD CONSTRAINT orders_unique_title UNIQUE (title);
```