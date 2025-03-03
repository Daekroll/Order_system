from smtplib import SMTPException

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import logging
from celery import shared_task

from ..models import Orders

logger_console = logging.getLogger('console_logger')
logger_file = logging.getLogger('file_logger')
"""
Документация по задачам Celery: 
https://docs.celeryq.dev/en/stable/userguide/tasks.html
"""


@shared_task
def log_order_creation(order: Orders):
    """
    Асинхронная задача Celery для обработки создания заказа.

    Выполняет:
    1. Генерацию HTML-письма с информацией о заказе
    2. Отправку письма клиенту на email
    3. Логирование события в консоль

    Параметры:
    - order (Orders): Созданный объект заказа

    Использует шаблон:
    - 'email/email_templates.html' с контекстом:
        {
            'order_pk': ID заказа
        }

    Пример письма:
    Тема: "Заказ № 123 создан"
    Тело: HTML-содержимое из шаблона с номером заказа
    """
    order_pk = order.id
    customer_email = order.customer_email
    context = {
        'order_pk': order_pk,
    }
    html_message = render_to_string('email/email_templates.html', context)
    email = EmailMessage(
        f'Заказ № {order_pk} создан',  # Тема письма
        html_message,
        [customer_email],  # Список получателей
    )
    email.content_subtype = "html"  # Указываем, что письмо содержит HTML
    try:
        email.send()
        logger_console.info(f'Заказ № {order_pk} создан')
    except SMTPException as e:
        logger_file.error(f"Ошибка отправки письма для заказа {order_pk}: {str(e)}")


@shared_task
def log_order_updated(order: Orders):
    """
    Асинхронная задача Celery для обработки обновления статуса заказа.

    Выполняет:
    1. Генерацию HTML-письма с новым статусом заказа
    2. Отправку письма клиенту
    3. Логирование изменения статуса в консоль

    Параметры:
    - order (Orders): Обновленный объект заказа с новым статусом

    Использует шаблон:
    - 'email/update_order.html' с контекстом:
        {
            'order_pk': ID заказа,
            'status': текущий статус заказа
        }

    Пример письма:
    Тема: "Заказ № 123 обновлен"
    Тело: HTML с номером заказа и новым статусом (например, "в обработке")
    """
    order_pk = order.id
    customer_email = order.customer_email
    status = order.status
    context = {
        'order_pk': order_pk,
        'status': status
    }
    html_message = render_to_string('email/update_order.html', context)
    email = EmailMessage(
        f'Заказ № {order_pk} обновлен',  # Тема письма
        html_message,
        [customer_email],  # Список получателей
    )
    email.content_subtype = "html"  # Указываем, что письмо содержит HTML
    try:
        email.send()
        logger_console.info(f'Статус заказа № {order_pk} изменен')
    except SMTPException as e:
        logger_file.error(f"Ошибка отправки письма для заказа {order_pk}: {str(e)}")
