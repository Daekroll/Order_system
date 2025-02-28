from celery import shared_task
import logging

logger_console = logging.getLogger('console_logger')
logger_file = logging.getLogger('file_logger')

@shared_task
def log_order_creation(order_id: int):
    logger_console.info(f'Заказ № {order_id} создан')


@shared_task
def log_order_updated(order_id: int):
    logger_console.info(f'Статус заказа № {order_id} изменен')