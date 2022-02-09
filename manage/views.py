from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

from users.models import User
from .models import Staff, Customer, Product, Order, Delivery
from .forms import StaffForm, CustomerForm, ProductForm, OrderForm, DeliveryForm


# Staff
@login_required(login_url='auth')
def create_staff(request):
    forms = StaffForm()
    if request.method == 'POST':
        forms = StaffForm(request.POST)
        if forms.is_valid():
            name = forms.cleaned_data['name']
            address = forms.cleaned_data['address']
            email = forms.cleaned_data['email']
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            retype_password = forms.cleaned_data['retype_password']
            if password == retype_password:
                user = User.objects.create_user(
                    username=username, password=password,
                    email=email, is_staff=True
                )
                Staff.objects.create(user=user, name=name, address=address)
                return redirect('staff-list')
    context = {
        'form': forms
    }
    return render(request, 'dashboard/create_staff.html', context)


class StaffListView(ListView):
    model = Staff
    template_name = 'dashboard/staff_list.html'
    context_object_name = 'staff'


# Customer
@login_required(login_url='auth')
def create_customer(request):
    forms = CustomerForm()
    if request.method == 'POST':
        forms = CustomerForm(request.POST)
        if forms.is_valid():
            name = forms.cleaned_data['name']
            address = forms.cleaned_data['address']
            email = forms.cleaned_data['email']
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            retype_password = forms.cleaned_data['retype_password']
            if password == retype_password:
                user = User.objects.create_user(
                    username=username, password=password,
                    email=email, is_customer=True
                )
                Customer.objects.create(user=user, name=name, address=address)
                return redirect('customer-list')
    context = {
        'form': forms
    }
    return render(request, 'dashboard/create_customer.html', context)


class CustomerListView(ListView):
    model = Customer
    template_name = 'dashboard/customer_list.html'
    context_object_name = 'customer'


# Product
@login_required(login_url='auth')
def create_product(request):
    forms = ProductForm()
    if request.method == 'POST':
        forms = ProductForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('product-list')
    context = {
        'form': forms
    }
    return render(request, 'dashboard/create_product.html', context)


class ProductListView(ListView):
    model = Product
    template_name = 'dashboard/product_list.html'
    context_object_name = 'product'


# Order
@login_required(login_url='auth')
def create_order(request):
    forms = OrderForm()
    if request.method == 'POST':
        forms = OrderForm(request.POST)
        if forms.is_valid():
            staff = forms.cleaned_data['staff']
            product = forms.cleaned_data['product']
            quantity = forms.cleaned_data['quantity']
            toppings = forms.cleaned_data['toppings']
            description = forms.cleaned_data['description']
            customer = forms.cleaned_data['customer']
            Order.objects.create(
                staff=staff,
                product=product,
                quantity=quantity,
                toppings=toppings,
                description=description,
                customer=customer,
                status='pending'
            )
            return redirect('order-list')
    context = {
        'form': forms
    }   # TODO HTML
    return render(request, 'dashboard/', context)


class OrderListView(ListView):
    model = Order   # TODO HTML
    template_name = 'dashboard/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.all().order_by('-id')
        return context

# TODO UPDATE ORDER

# Delivery
@login_required(login_url='auth')
def create_delivery(request):
    forms = DeliveryForm()
    if request.method == 'POST':
        forms = DeliveryForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('delivery-list')
    context = {
        'form': forms
    }   # TODO HTML
    return render(request, 'dashboard/', context)


class DeliveryListView(ListView):
    model = Delivery
    template_name = 'dashboard/'   # TODO HTML
    context_object_name = 'delivery'


