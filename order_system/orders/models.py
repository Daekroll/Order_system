from django.db import models
from django.core.validators import validate_email


class Orders(models.Model):
    status_list = [
        ('created', 'created'),
        ('processing', 'processing'),
        ('completed', 'completed'),
        ('cancelled', 'cancelled')
    ]



    product_name = models.CharField(max_length=30, blank=False, null=False, verbose_name='Наименование продукта')
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name='Количество')
    customer_email = models.EmailField(max_length=255, validators=[validate_email], verbose_name='Электронная почта')
    status = models.CharField(max_length=10, default='created', choices=status_list, verbose_name='Статус заказа')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата и время обновления')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказ'

    def __str__(self):
        return f'Order id: {self.pk}, product: {self.product_name}'
