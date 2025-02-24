from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework.urls import app_name

from .views import OrdersApiView

app_name = 'orders'

router = DefaultRouter()

router.register('v1/orders', OrdersApiView, basename='orders')

urlpatterns = [
    path('', include(router.urls)),
]
