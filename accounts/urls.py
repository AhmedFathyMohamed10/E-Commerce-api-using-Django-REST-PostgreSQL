from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/', views.RegisterView.as_view(), name='sign-up'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]