# notification_service_app

Проект сервиса уведомлений

Использовался следующий стэк

```
- Celery
- Django
- django_celery_beat
- django_phonenumber_field
- Django Rest Framework
- drf-yasg
- psycopg2
- pip-compile-multi
- python-dotenv
- redis
```

## Установка и запуск(локально):

1. Скачать проект

   - git clone https://github.com/scad89/notification_service_app.git

2. Добавить файл с переменными окружения(.env) в корень проекта

3. Активировать виртуальное окружение:

   - . venv_name/Scripts/activate - Windows
   - source venv_name/bin/activate - Linux

4. Установить зависимости(в виртуальном окружении):

   - pip-compile -U
   - pip install -r requirements.txt

5. Сделать миграции:

   - python manage.py makemigrations
   - python manage.py migrate

6. Создать суперпользователя для администраторского Web UI:

   - python manage.py createsuperuser

7. Загрузить фикстуры(дефолтные значения клиентов):

   - python manage.py loaddata main_fixtures.json

8. Запустить сервер:

   - python manage.py runserver

9. Запустить Celery в отдельном терминале:

   - celery -A notification_service worker -l info

10. Запустить flower в отдельном терминале:

- celery -A notification_service flower --port=5555

```
http://127.0.0.1:5555 -по этому адресу можно открыть flower
```

## Установка и запуск(docker-compose):

1. Добавить файл с переменными окружения(.env_docker) в корень проекта
2. Запустить командой:
   - sudo docker-compose up -d

Если необходимо пересобрать контейнеры(внесли какие-то изменения) использовать:

- sudo docker-compose up -d

Если Вы запускаете проект на Windows, а docker из-под виртуальной машины(по типу VirtualBox), проект
по адресу 0.0.0.0:8000 может не открыться. Тогда необходимо использовать 192.168.99.100:8000

Для остановки контейнеров используйте команду:

```
docker-compose down -v
```

## Описание методов и документация:

```
http://127.0.0.1:8000/docs/
```

### Дополнительно реализовано:

- подготовить docker-compose для запуска всех сервисов проекта одной командой(пункт №3)
- документация(пункт №5)
- администраторский Web UI (http://127.0.0.1:8000/admin/)(пункт №6)
- обработка ошибок удалённого сервера и создание статуса 'Error' сообщения с последующим созданием периодической задачи(пункт №9)
- реализована дополнительная возможность отправки уведомлений клиентам в зависимости от часового пояса клиента. Если время не соответствует необходимому диапазону, задача получает статус 'Wrong Time' и будет повторно запущена через 1 час(пункт №11)

#### В процессе реализации:

- организовать тестирование написанного кода(пункт №2)
- обеспечить интеграцию с внешним OAuth2 сервисом авторизации для административного интерфейса. Пример: https://auth0.com (пункт №7)
- реализовать дополнительный сервис, который раз в сутки отправляет статистику по обработанным рассылкам на email(пункт №8)
- реализовать отдачу метрик в формате prometheus и задокументировать эндпоинты и экспортируемые метрики(пункт №10)
- обеспечить подробное логирование на всех этапах обработки запросов, чтобы при эксплуатации была возможность найти в логах всю информацию по(пункт №12):
  - id рассылки - все логи по конкретной рассылке (и запросы на api и внешние запросы на отправку конкретных сообщений)
  - id сообщения - по конкретному сообщению (все запросы и ответы от внешнего сервиса, вся обработка конкретного сообщения)
  - id клиента - любые операции, которые связаны с конкретным клиентом (добавление/редактирование/отправка сообщения/…)

##### Исправлено

1. Нейминг периодических задач. Не могла поставиться периодическая задача на рассылку уведомления для двух разных клиентов.
2. Ссылка на внешний сервис в _.env_ файле. При локальном запуске проекта проблем никаких не было, но если проект запускался с помощью docker-compose, возникала ошибка _requests.exceptions.InvalidSchema: No connection adapters were found for_ .

## Contacts

- Instagram: [@igor*komkov*](https://www.instagram.com/igor_komkov_/)
- Vk.com: [Igor Komkov](https://vk.com/zzzscadzzz)
- Linkedin: [Igor Komkov](https://www.linkedin.com/in/igor-komkov/)
- email: **scad200@gmail.com**
