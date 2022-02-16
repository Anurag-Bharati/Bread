from django.urls import path
from . import views
from .views import GetProduct

urlpatterns = [
    path('', views.home_page, name='home-page'),
    path('products/', GetProduct.as_view(), name='products'),
    path('order/<int:id>', views.order, name="order"),
    path('my-plate/', views.my_plate, name="my-plate"),
    path('profile/', views.my_profile, name="customer-profile"),
    path('update-profile/', views.edit_profile, name="update-profile"),
]
