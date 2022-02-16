from django.shortcuts import render

# Create your views here.
from manage.models import Staff, Product, Customer, Delivery


def home(request):
    staff_count = Staff.objects.all().count()
    product_count = Product.objects.all().count()
    customer_count = Customer.objects.all().count()
    delivery_count = Delivery.objects.all().count()
    context = {
        'customer_count': customer_count,
        'staff_count': staff_count,
        'product_count': product_count,
        'delivery_count': delivery_count
    }
    return render(request, 'home.html', context)
