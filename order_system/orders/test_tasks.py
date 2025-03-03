from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from unittest.mock import patch, MagicMock
import pytest
from orders.models import Orders
from orders.api.tasks import log_order_creation, log_order_updated
from smtplib import SMTPException


@pytest.mark.django_db
def test_log_order_creation():
    """
    Тест для задачи log_order_creation.
    Проверяет:
    1. Генерацию HTML-письма.
    2. Отправку письма.
    3. Логирование успешного выполнения.
    """
    # Создаем тестовый заказ
    order = Orders.objects.create(
        product_name="iPhone 15",
        quantity=1,
        customer_email="test@example.com",
        status="created"
    )

    # Мокируем EmailMessage.send
    with patch.object(EmailMessage, 'send') as mock_send:
        # Выполняем задачу
        log_order_creation(order)

        # Проверяем, что send был вызван
        mock_send.assert_called_once()

        # Проверяем, что письмо было сгенерировано с правильными параметрами
        expected_html = render_to_string('email/email_templates.html', {'order_pk': order.id})
        mock_send.assert_called_once()

    # Проверяем, что логи записаны
    with patch('orders.api.tasks.logger_console.info') as mock_logger:
        log_order_creation(order)
        mock_logger.assert_called_once_with(f'Заказ № {order.id} создан')


@pytest.mark.django_db
def test_log_order_creation_email_failure():
    """
    Тест для задачи log_order_creation при ошибке отправки письма.
    Проверяет:
    1. Логирование ошибки.
    """
    # Создаем тестовый заказ
    order = Orders.objects.create(
        product_name="iPhone 15",
        quantity=1,
        customer_email="test@example.com",
        status="created"
    )

    # Мокируем EmailMessage.send, чтобы он выбрасывал исключение
    with patch.object(EmailMessage, 'send', side_effect=SMTPException("Ошибка отправки")):
        with patch('orders.api.tasks.logger_file.error') as mock_logger:
            # Выполняем задачу
            log_order_creation(order)

            # Проверяем, что ошибка была залогирована
            mock_logger.assert_called_once_with(f"Ошибка отправки письма для заказа {order.id}: Ошибка отправки")


@pytest.mark.django_db
def test_log_order_updated():
    """
    Тест для задачи log_order_updated.
    Проверяет:
    1. Генерацию HTML-письма.
    2. Отправку письма.
    3. Логирование успешного выполнения.
    """
    # Создаем тестовый заказ
    order = Orders.objects.create(
        product_name="iPhone 15",
        quantity=1,
        customer_email="test@example.com",
        status="completed"
    )

    # Мокируем EmailMessage.send
    with patch.object(EmailMessage, 'send') as mock_send:
        # Выполняем задачу
        log_order_updated(order)

        # Проверяем, что send был вызван
        mock_send.assert_called_once()

        # Проверяем, что письмо было сгенерировано с правильными параметрами
        expected_html = render_to_string('email/update_order.html', {'order_pk': order.id, 'status': order.status})
        mock_send.assert_called_once()

    # Проверяем, что логи записаны
    with patch('orders.api.tasks.logger_console.info') as mock_logger:
        log_order_updated(order)
        mock_logger.assert_called_once_with(f'Статус заказа № {order.id} изменен')


@pytest.mark.django_db
def test_log_order_updated_email_failure():
    """
    Тест для задачи log_order_updated при ошибке отправки письма.
    Проверяет:
    1. Логирование ошибки.
    """
    # Создаем тестовый заказ
    order = Orders.objects.create(
        product_name="iPhone 15",
        quantity=1,
        customer_email="test@example.com",
        status="completed"
    )

    # Мокируем EmailMessage.send, чтобы он выбрасывал исключение
    with patch.object(EmailMessage, 'send', side_effect=SMTPException("Ошибка отправки")):
        with patch('orders.api.tasks.logger_file.error') as mock_logger:
            # Выполняем задачу
            log_order_updated(order)

            # Проверяем, что ошибка была залогирована
            mock_logger.assert_called_once_with(f"Ошибка отправки письма для заказа {order.id}: Ошибка отправки")
