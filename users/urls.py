from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('loguot', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('user_recipes', views.user_recipes, name='user_recipes'),
]