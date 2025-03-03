import os
from celery import Celery

"""
Celery Configuration for Django Project

Этот файл инициализирует и настраивает Celery для работы с Django. 
Он выполняет:
1. Установку переменной окружения для доступа к настройкам Django.
2. Создание экземпляра приложения Celery.
3. Загрузку настроек из `settings.py` (с префиксом `CELERY_*`).
4. Автоматическое обнаружение задач в файлах `tasks.py` всех Django-приложений.

Важные параметры:
- `broker_connection_retry_on_startup=True`: повторные попытки подключения к брокеру (RabbitMQ/Redis) при старте.
- `namespace='CELERY'`: указывает, что настройки Celery в `settings.py` начинаются с `CELERY_*`.

Примеры настроек в `settings.py`:
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
"""
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'order_system.settings')

app = Celery('order_system',
             broker_connection_retry_on_startup=True
             )
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
