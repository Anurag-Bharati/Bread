from django.urls import path
from . import views

urlpatterns = [
    path('', views.authenticate, name="auth"),
    path('lol/', views.home),
]
