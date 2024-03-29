# Домашнее задание к занятию 2. «Облачные провайдеры и синтаксис Terraform»
Зачастую разбираться в новых инструментах гораздо интереснее, если понимаешь, как они работают изнутри. Поэтому в рамках первого необязательного задания предлагаем завести свою учётную запись в AWS (Amazon Web Services) или Yandex.Cloud. Идеально будет познакомиться с обоими облаками, потому что они отличаются.

### Задача 1 (вариант с AWS). Регистрация в AWS и знакомство с основами (не обязательно, но крайне желательно)
Остальные задания можно будет выполнять и без этого аккаунта, но с ним можно будет увидеть полный цикл процессов.

AWS предоставляет много бесплатных ресурсов в первый год после регистрации, подробно описано [здесь](https://aws.amazon.com/free/)

1) Создайте аккаунт AWS.
2) Установите c [aws-cli](https://aws.amazon.com/cli/)
3) Выполните первичную настройку [aws-sli.](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)
4) Создайте IAM-политику для Terraform c правами:
   * AmazonEC2FullAccess,
   * AmazonS3FullAccess,
   * AmazonDynamoDBFullAccess,
   * AmazonRDSFullAccess,
   * CloudWatchFullAccess,
   * IAMFullAccess.
5) Добавьте переменные окружения
```
export AWS_ACCESS_KEY_ID=(your access key id)
export AWS_SECRET_ACCESS_KEY=(your secret access key).
```
6) Создайте, остановите и удалите ec2-инстанс (любой с пометкой `free tier`) через веб-интерфейс.
В виде результата задания приложите вывод команды `aws configure list`.

### Задача 1 (вариант с Yandex.Cloud). Регистрация в Яндекс Облаке и знакомство с основами (не обязательно, но крайне желательно)
1) Подробная инструкция на русском языке лежит [здесь.](https://cloud.yandex.ru/docs/solutions/infrastructure-management/terraform-quickstart)
2) Обратите внимание на период бесплатного использования после регистрации аккаунта.
3) Используйте раздел «Подготовьте облако к работе» для регистрации аккаунта. Далее раздел «Настройте провайдер» для подготовки базового Terraform-конфига.
4) Воспользуйтесь [инструкцией](https://registry.terraform.io/providers/yandex-cloud/yandex/latest/docs) на сайте Terraform, чтобы не указывать авторизационный токен в коде, а Terraform-провайдер брал его из переменных окружений.
### Задача 2. Создание AWS ec2 или yandex _compute _instance через Terraform
1) В каталоге `Terraform` вашего основного репозитория, который был создан в начале курсе, создайте файл `main.tf` и `versions.tf`.

2) Зарегистрируйте провайдер:

   * Для [AWS](https://registry.terraform.io/providers/hashicorp/aws/latest/docs). В файл `main.tf` добавьте блок `provider`, а в `versions.tf` блок `Terraform` с вложенным блоком `required_providers`. Укажите любой выбранный вами регион внутри блока `provider`.
либо

2) Для [Yandex.Cloud](https://registry.terraform.io/providers/yandex-cloud/yandex/latest/docs). Подробную инструкцию можно найти [здесь](https://cloud.yandex.ru/docs/solutions/infrastructure-management/terraform-quickstart).
3) Внимание. В git-репозиторий нельзя пушить ваши личные ключи доступа к аккаунту. Поэтому в предыдущем задании мы указывали их в виде переменных окружения.
4) В файле `main.tf` воспользуйтесь блоком `data "aws_ami` для поиска ami-образа последнего Ubuntu.
5) В файле `main.tf` создайте ресурс
   * либо [ec2 instance](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance). Постарайтесь указать как можно больше параметров для его определения. Минимальный набор параметров указан в первом блоке Example Usage, но желательно указать большее количество параметров.
   * либо [yandex _compute _image](https://registry.terraform.io/providers/yandex-cloud/yandex/latest/docs/resources/compute_image).
6) Также в случае использования AWS:
   * Добавьте data-блоки `aws_caller_identity` и `aws_region`.
   * В файл `outputs.tf` поместите блоки `output` с данными об используемых в данный момент:
     * AWS account ID;
     * AWS user ID;
     * AWS регион, который используется сейчас;
     * Приватный IP ec2-инстансы;
     * Идентификатор подсети, в которой создан инстанс.
7) Если вы выполнили первый пункт, то добейтесь того, что бы команда `terraform plan` выполнялась без ошибок.

В качестве результата задания предоставьте:

1) Ответ на вопрос, при помощи какого инструмента из разобранных на прошлом занятии можно создать свой образ ami.
2) Ссылку на репозиторий с исходной конфигурацией Terraform.
### Как cдавать задание
Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.