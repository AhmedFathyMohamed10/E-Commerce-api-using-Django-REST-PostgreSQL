from django.urls import path
from django.conf.urls import handler404
from . import views
from .views import custom_404_view

handler404 = custom_404_view

urlpatterns = [
    path('sign-up/', views.RegisterView.as_view(), name='sign-up'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]