from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('login/', views.login_view, name='login'),
]
