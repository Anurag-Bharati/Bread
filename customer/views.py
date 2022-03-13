from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib import messages, auth
from django.views.decorators.cache import cache_control
from django.views.generic import ListView

from manage.forms import OrderForm, CustomerUpdateForm
from manage.models import Product, Customer, Order


def home_page(request):
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
    paginate_by = 5
    context_object_name = 'products'

    def get_queryset(self):

        filter_val = self.request.GET.get('name_contains', None)
        if filter_val == 'featured':
            new_context = Product.objects.filter(is_featured__exact=True)
        elif filter_val == 'new':
            new_context = Product.objects.all().order_by('-id')
        elif filter_val and not filter_val == '#' and not str(filter_val).lower() == 'all':
            new_context = Product.objects.filter(
                name__icontains=filter_val,
            )
        else:
            new_context = Product.objects.all().order_by('id')
        return new_context

    def get_context_data(self, **kwargs):
        context = super(GetProduct, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_anonymous:
            context['user'] = None
        else:
            context['user'] = user
        context['filter'] = self.request.GET.get('name_contains', None)
        context['search'] = self.request.GET.get('name_contains', None)
        context['specials'] = Product.objects.filter(is_special=True).order_by('-id')
        return context


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, "Logged out successfully")
        return redirect('auth')


@login_required(login_url='auth')
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
        forms = CustomerUpdateForm(initial={
            'name': customer.name,
            'address': customer.address,
            'image': customer.image
        })
        context = {
            'form': forms
        }
        return render(request, 'customer/update_profile.html', context)

    elif request.method == 'POST':

        name = request.POST['name']
        address = request.POST['address']

        if name and name != customer.name:
            if Customer.objects.filter(name__exact=name):
                messages.error(request, 'Name ' + name + ' is already taken.')
                return redirect('update-profile')
            customer.name = name

        image = request.FILES.get('image', None)

        if image and image.name != customer.image.name:
            customer.image = image

        if address and address != customer.address:
            customer.address = address

        customer.save()
        messages.success(request, 'Profile updated  successfully')
        return redirect('customer-profile')
