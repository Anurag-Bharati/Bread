from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib import messages
from manage.forms import OrderForm
from manage.models import Product, Customer, Order

@login_required(login_url='auth')
def home_page(request):
    return render(request, 'customer/customer_home.html')

@login_required(login_url='auth')
def order(request, id):
    if request.method == 'GET':
        form = OrderForm()
        product = Product.objects.get(id=id)
        context = {
            'form': form,
            'id': id
        }
        if product and product.price is not None:
            context['product'] = product
        return render(request, 'customer/order.html', context)

    elif request.method == 'POST':
        form = OrderForm(request.POST)
        customer = Customer.objects.get(id=request.user.id)
        product = Product.objects.get(id=id)
        quantity = request.POST['quantity']
        toppings = request.POST['toppings']
        description = request.POST['description']
        context = {
            'form': form,
            'id': id
        }
        if not customer:
            messages.error(request, "Sorry, This service is only for customers")
            return render(request, 'customer/order.html', context)
        elif not product:
            messages.error(request, "The specified product could not be found")
            return render(request, 'customer/order.html', context)
        elif not quantity or int(quantity) < 1:
            messages.error(request, "Please, Select a valid quantity")
            return render(request, 'customer/order.html', context)

        Order.objects.create(
            staff=None,
            product=product,
            quantity=quantity,
            toppings=toppings,
            description=description,
            customer=customer,
            status='pending'
        )
        return redirect('my-plate')

def my_plate(request):
    if request.method == 'GET':
        orders = Order.objects.filter(customer=request.user.id).order_by('-id')

        pending = orders.filter(status__exact='pending')
        approved = orders.filter(status__exact='approved')
        processing = orders.filter(status__exact='processing')

        complete = orders.filter(status__exact='complete')
        declined = orders.filter(status__exact='decline')

        active_orders = pending | approved | processing

        passive_orders = complete | declined

        context = {
            'order': active_orders,
            'passive_order': passive_orders
        }

        return render(request, 'customer/my_orders.html', context)
