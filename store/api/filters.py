import django_filters
from store.models import Product

class ProductFilter(django_filters.FilterSet):
    """
    Custom filter class for Product model.
    Allows filtering by category slug using the simple 'category' parameter.
    """
    category = django_filters.CharFilter(
        field_name='category__slug',
        lookup_expr='exact'
    )

    class Meta:
        model = Product
        fields = ['category']
