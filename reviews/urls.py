from django.urls import path
from .views import ReviewCreateView


urlpatterns = [
    path('products/<int:pk>/create-review', ReviewCreateView.as_view(), name='create-review'),
    # path('product/<int:product_id>/', ReviewListView.as_view(), name='product-reviews'),
    # path('product/<int:pk>/details/', ProductReviewDetailView.as_view(), name='product-review-details'),
]