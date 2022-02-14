from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib import messages, auth
from django.views.decorators.cache import cache_control
from django.views.generic import ListView

from manage.forms import OrderForm, CustomerForm
from manage.models import Product, Customer, Order


@login_required(login_url='auth')
def home_page(request):
    if request.user.is_staff:
        return redirect('dashboard')

    return redirect('products')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='auth')
def order(request, id):

    if request.user.is_staff:
        return redirect('dashboard')
    if request.method == 'GET':
        form = OrderForm(request.GET)
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
        customer = Customer.objects.get(id=request.user.customer.id)
        product = Product.objects.get(id=id)
        quantity = request.POST['quantity']
        toppings = request.POST['toppings']
        description = request.POST['description']
        context = {
            'form': form,
            'id': id
        }
        if product and product.price is not None:
            context['product'] = product
        if request.user.is_staff:
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

@login_required(login_url='auth')
def my_plate(request):
    if request.user.is_staff:
        return redirect('dashboard')
    if request.method == 'GET':
        orders = Order.objects.filter(customer=request.user.customer.id).order_by('-id')

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

class GetProduct(ListView):
    model = Product
    template_name = 'customer/customer_home.html'
    context_object_name = 'products'
    paginate_by = 1

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, "Logged out successfully")
        return redirect('auth')


def my_profile(request):
    context = {
        'user': request.user,
        'total_order': Order.objects.filter(customer=request.user.customer.id).count()
    }
    return render(request, 'customer/my-profile.html', context)

@login_required(login_url='/auth')
def edit_profile(request):
    if request.user.is_staff:
        return redirect('dashboard')
    customer = Customer.objects.get(pk=request.user.customer.id)
    if request.method == 'GET':
        forms = CustomerForm(initial={
            'name': customer.name,
            'address': customer.address,
            'email': customer.user.email,
            'username': customer.user.username,
            'image': customer.profile_pic.url,
        })
        context = {
            'form': forms
        }
        return render(request, 'customer/update_profile.html', context)

    elif request.method == 'POST':
        forms = CustomerForm(request.POST, request.FILES)

        name = request.POST['name']
        address = request.POST['address']
        email = request.POST['email']
        username = request.POST['username']
        image = request.FILES['image']

        if name and name != customer.name:
            if Customer.objects.filter(name__exact=name):
                context = {'form': forms}
                messages.error(request, 'The name is already taken.')
                return render(request, 'customer/update_profile.html', context)
            customer.name = name
        if address and address != customer.address:
            customer.address = address
        if email and email != customer.user.email:
            customer.user.email = email
        if username and username != customer.user.username:
            customer.user.username = username
        if image and image != customer.profile_pic:
            customer.profile_pic = image

        customer.save()
        messages.success(request, 'Profile updated  successfully')
        return redirect('customer-profile')
