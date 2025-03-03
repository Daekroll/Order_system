from django.db import models
from django.core.validators import validate_email
from rest_framework.exceptions import ValidationError


def validate_quantity_zero(quantity):
    """
    Валидатор для проверки, что значение количества не равно нулю или меньше.

    Args:
        quantity (int): Количество товара.

    Raises:
        ValidationError: Если количество меньше или равно нулю.
    """
    if quantity <= 0:
        raise ValidationError('This fields cannot be zero')


class Orders(models.Model):
    """
    Модель, представляющая заказ.

    Атрибуты:
        status_list (list): Список возможных статусов заказа.
        product_name (CharField): Наименование продукта (максимум 30 символов).
        quantity (PositiveSmallIntegerField): Количество товара (по умолчанию 1, не может быть нулевым или отрицательным).
        customer_email (EmailField): Электронная почта покупателя (валидируется на корректность).
        status (CharField): Статус заказа (по умолчанию 'created').
        created_at (DateTimeField): Дата и время создания заказа (автоматически добавляется при создании).
        update_at (DateTimeField): Дата и время обновления заказа (автоматически обновляется при изменении).

    Мета:
        verbose_name (str): Человекочитаемое имя модели в единственном числе.
        verbose_name_plural (str): Человекочитаемое имя модели во множественном числе.

    Методы:
        __str__: Возвращает строковое представление заказа в формате "Order id: {id}, product: {product_name}".
    """
    status_list = [
        ('created', 'created'),
        ('processing', 'processing'),
        ('completed', 'completed'),
        ('cancelled', 'cancelled')
    ]

    product_name = models.CharField(max_length=30, blank=False, null=False, verbose_name='Наименование продукта')
    quantity = models.PositiveSmallIntegerField(default=1, validators=[validate_quantity_zero], verbose_name='Количество')
    customer_email = models.EmailField(max_length=255, validators=[validate_email], verbose_name='Электронная почта')
    status = models.CharField(max_length=10, default='created', choices=status_list, verbose_name='Статус заказа')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата и время обновления')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказ'

    def __str__(self):
        return f'Order id: {self.pk}, product: {self.product_name}'
