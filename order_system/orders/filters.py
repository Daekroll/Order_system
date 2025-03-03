import django_filters
from .models import Orders

class OrdersFilter(django_filters.FilterSet):
    # Поиск по точному совпадению для поля `status`
    status = django_filters.CharFilter(lookup_expr='iexact')

    # Поиск по частичному совпадению для поля `product_name`
    product_name = django_filters.CharFilter(lookup_expr='icontains')

    # Поиск по частичному совпадению для поля `customer_email`
    customer_email = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Orders
        fields = ['status', 'product_name', 'customer_email']