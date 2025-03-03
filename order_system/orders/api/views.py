import logging

import django_filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import OrdersSerializer, OrdersCreateSerializer, OrdersUpdateSerializer
from orders.models import Orders
from orders.filters import OrdersFilter
from .tasks import log_order_creation, log_order_updated
logger1 = logging.getLogger('console_logger')
logger2 = logging.getLogger('file_logger')


class OrdersApiView(ModelViewSet):
    """
    API endpoint для управления заказами.

    Поддерживает операции создания, обновления, получения и удаления заказов.
    Использует разные сериализаторы в зависимости от типа операции:
    - OrdersSerializer для чтения данных
    - OrdersCreateSerializer для создания заказов
    - OrdersUpdateSerializer для обновления заказов
    """
    queryset = Orders.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = OrdersFilter
    def get_serializer_class(self):
        """
        Определяет подходящий сериализатор в зависимости от HTTP-метода:
        - GET: OrdersSerializer (отображение данных)
        - POST: OrdersCreateSerializer (создание заказа)
        - PUT/PATCH: OrdersUpdateSerializer (обновление заказа)
        """
        if self.request.method == 'GET':
            return OrdersSerializer
        if self.request.method == 'POST':
            return OrdersCreateSerializer
        else:
            return OrdersUpdateSerializer

    def create(self, request, *args, **kwargs):
        """
        Создает новый заказ.

        При успешной валидации:
        - Сохраняет заказ в БД
        - Запускает асинхронную задачу log_order_creation
        - Логирует событие в консоль
        Возвращает сериализованные данные заказа с статусом 201.
        При ошибке валидации возвращает 400.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            instance = serializer.save()
            full_serializer = OrdersSerializer(instance)
            log_order_creation.delay(full_serializer.data)
            logger1.info(f'Заказ № {full_serializer.data.get('id')} создан')
            return Response(full_serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Обновляет существующий заказ.

        Использует частичное обновление (PATCH). При успешной валидации:
        - Сохраняет изменения в БД
        - Запускает асинхронную задачу log_order_updated
        - Логирует событие в консоль
        Возвращает обновленные данные заказа с статусом 200.
        При ошибке валидации возвращает 400.
        """
        instance = self.get_object()
        update_serializer = self.get_serializer(instance, data=request.data, partial=True)

        if update_serializer.is_valid():
            update_serializer.save()
            full_serializer = OrdersSerializer(instance)
            log_order_updated.delay(full_serializer.data)
            logger1.info(f'Статус заказа № {full_serializer.data.get('id')} изменен')
            return Response(full_serializer.data, status=status.HTTP_200_OK)

        return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)