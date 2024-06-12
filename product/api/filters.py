import django_filters
from product.models import Product

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    p_type = django_filters.CharFilter(field_name='p_type', lookup_expr='exact')
    min_price = django_filters.NumberFilter(field_name='productline__price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='productline__price', lookup_expr='lte')
    category = django_filters.CharFilter(field_name='productline__category__name', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['name', 'p_type', 'min_price', 'max_price', 'category']