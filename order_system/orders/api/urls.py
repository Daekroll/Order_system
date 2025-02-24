from rest_framework.routers import DefaultRouter
from django.urls import path, include


from .views import OrdersApiView

router = DefaultRouter()

router.register('v1/orders', OrdersApiView, basename='orders')

urlpatterns = [
    path('', include(router.urls)),
]
