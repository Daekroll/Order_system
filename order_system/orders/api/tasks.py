from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import logging
from celery import shared_task

from ..models import Orders
logger_console = logging.getLogger('console_logger')
logger_file = logging.getLogger('file_logger')

@shared_task
def log_order_creation(order: Orders):
    order_pk = order.pk
    customer_email = order.customer_email
    context = {
        'order_pk':order_pk,
               }
    html_message = render_to_string('email/email_template.html',context)
    email = EmailMessage(
        f'Заказ № {order_pk} создан',  # Тема письма
        html_message,
        [customer_email],  # Список получателей
    )
    email.content_subtype = "html"  # Указываем, что письмо содержит HTML
    email.send()

    logger_console.info(f'Заказ № {order_pk} создан')


@shared_task
def log_order_updated(order: Orders):
    order_pk = order.pk
    customer_email = order.customer_email
    status = order.status
    context = {
        'order_pk': order_pk,
        'status':status
    }
    html_message = render_to_string('email/update_order.html', context)
    email = EmailMessage(
        f'Заказ № {order_pk} обновлен',  # Тема письма
        html_message,
        [customer_email],  # Список получателей
    )
    email.content_subtype = "html"  # Указываем, что письмо содержит HTML
    email.send()
    logger_console.info(f'Статус заказа № {order_pk} изменен')