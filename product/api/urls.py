from django.urls import path
from .api_views import ProductList, ProductDetail, CategoryList

urlpatterns = [
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    # ---------------------------------------------------------------------------
    path('categories/', CategoryList.as_view(), name='categories-list'),
]
