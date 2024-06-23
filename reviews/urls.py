from django.urls import path
from .views import ReviewCreateView, ReviewGetView


urlpatterns = [
    path('products/<int:pk>/create-review', ReviewCreateView.as_view(), name='create-review'),
    path('reviews/', ReviewGetView.as_view(), name='get-review')
]