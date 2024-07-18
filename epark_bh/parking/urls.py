
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('user-home/', views.user_home, name='user_home'),
    path('logout/', views.user_logout, name='logout'),


]