from django.urls import path

from manage.views import GetProduct
from . import views

urlpatterns = [
    path('', GetProduct.as_view(), name='products'),

    path('order/<int:id>', views.order, name="order"),
    path('my-plate/', views.my_plate, name="my-plate"),


]
