from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from manage.models import Product, Staff, Customer, Order


@login_required(login_url='auth')
def dashboard(request):
    if not request.user.is_staff:
        return redirect('products')
    total_product = Product.objects.count()
    total_staff = Staff.objects.count()
    total_customer = Customer.objects.count()
    total_oder = Order.objects.count()
    orders = Order.objects.all().order_by('-id')
    orders = orders.filter(status__exact='pending')
    context = {
        'product': total_product,
        'staff': total_staff,
        'customer': total_customer,
        'order': total_oder,
        'orders': orders
    }
    return render(request, 'dashboard/dashboard.html', context)
