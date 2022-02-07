from django.urls import path
from . import views

urlpatterns = [
    path('', views.authenticate, name="auth"),
    path('activate/<identity>/<token>', views.verification, name="activate"),
    path('activate/', views.activated, name="activated"),
    path('logout/', views.logout, name="logout"),
]
