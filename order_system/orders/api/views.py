import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import OrdersSerializer, OrdersCreateSerializer, OrdersUpdateSerializer
from orders.models import Orders
from .tasks import log_order_creation, log_order_updated
logger1 = logging.getLogger('console_logger')
logger2 = logging.getLogger('file_logger')


class OrdersApiView(ModelViewSet):
    queryset = Orders.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrdersSerializer
        if self.request.method == 'POST':
            return OrdersCreateSerializer
        else:
            return OrdersUpdateSerializer

    def create(self, request, *args, **kwargs):
        serializer =  self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            instance = serializer.save()
            full_serializer = OrdersSerializer(instance)
            log_order_creation.delay(full_serializer.data.get('id'))
            logger1.info(f'Заказ № {full_serializer.data.get('id')} создан')
            return Response(full_serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        update_serializer = self.get_serializer(instance, data=request.data, partial=True)

        if update_serializer.is_valid():
            update_serializer.save()
            full_serializer = OrdersSerializer(instance)
            log_order_updated.delay(full_serializer.data.get('id'))
            logger1.info(f'Статус заказа № {full_serializer.data.get('id')} изменен')
            return Response(full_serializer.data, status=status.HTTP_200_OK)

        return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)