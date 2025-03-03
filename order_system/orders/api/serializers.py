from rest_framework import serializers
from orders.models import Orders

class OrdersSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для модели Orders.

    Используется для:
    - Отображения всех полей заказа
    - Вложенных представлений (если используется в related-полях других сериализаторов)

    Поля:
    __all__ - включаются все поля модели (ID, product_name, quantity, customer_email,
             status, created_at, updated_at и другие)
    """
    class Meta:
        model = Orders
        fields = '__all__'

class OrdersCreateSerializer(OrdersSerializer):
    """
    Специализированный сериализатор для СОЗДАНИЯ заказов.
    Наследует базовый OrdersSerializer, но ограничивает набор полей для безопасности.

    Разрешенные поля при создании:
    - product_name: Название товара (строка)
    - quantity: Количество (целое положительное число)
    - customer_email: Email клиента (валидируется автоматически)

    Не включает служебные поля (status, created_at и др.), которые устанавливаются автоматически.
    """
    class Meta(OrdersSerializer.Meta):
        fields = 'product_name', 'quantity', 'customer_email',

class OrdersUpdateSerializer(OrdersSerializer):
    """
    Специализированный сериализатор для ОБНОВЛЕНИЯ заказов.
    Позволяет изменять только статус заказа.

    Разрешенное поле для обновления:
    - status: Текущий статус заказа (выбор из значений: 'created', 'processing', 'completed', 'canceled')

    Остальные поля защищены от изменений после создания заказа.
    """
    class Meta(OrdersSerializer.Meta):
        fields = 'status',