from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from users.models import User
from .models import Staff, Customer, Product, Order, Delivery
from .forms import StaffForm, CustomerForm, ProductForm, OrderForm, DeliveryForm, EditOrderForm


# Staff views
@login_required(login_url='login')
def create_staff(request):
    if not request.user.is_staff:
        return redirect('products')
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
    if not request.user.is_staff:
        return redirect('products')
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
    if not request.user.is_staff:
        return redirect('products')
    forms = ProductForm()

    if request.method == 'POST':
        forms = ProductForm(request.POST, request.FILES)
        name = request.POST['name']

        if Product.objects.filter(name__exact=name):
            context = {
                'form': forms
            }
            messages.error(request, "Product named '" + name + "' already exists")
            return render(request, 'dashboard/create_product.html', context)
        if forms.is_valid():
            print(request.FILES)
            forms.save()
            messages.success(request, 'Product added successfully')
            return redirect('product-list')
        else:
            messages.error(request, 'Please, Provide valid data')
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
    if not request.user.is_staff:
        return redirect('products')
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
            messages.success(request, 'Order added successfully')
            return redirect('order-list')
        else:
            messages.error(request, 'Please, Provide valid data.')
    context = {
        'form': forms
    }

    return render(request, 'dashboard/create_order.html', context)


class OrderListView(ListView):
    model = Order
    template_name = 'dashboard/order_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.all().order_by('-id')
        return context


class ModifyOrder(ListView):
    model = Order
    template_name = 'dashboard/modify_order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.all().order_by('-id')
        return context


@login_required(login_url='/auth')
def edit_order(request, id):
    if not request.user.is_staff:
        return redirect('products')
    order = Order.objects.get(pk=id)
    if request.method == 'GET':
        forms = EditOrderForm(initial={
            'staff': order.staff,
            'customer': order.customer,
            'product': order.product,
            'quantity': order.quantity,
            'toppings': order.toppings,
            'description': order.description,
            'status': order.status
        })
        context = {
            'form': forms
        }
        return render(request, 'dashboard/edit-order.html', context)

    elif request.method == 'POST':
        forms = EditOrderForm(request.POST)
        if not forms.is_valid():
            context = {'form': forms}
            messages.error(request, 'Please, Provide valid data.')
            return render(request, 'dashboard/edit-order.html', context)

        staff = forms.cleaned_data['staff']
        product = forms.cleaned_data['product']
        customer = forms.cleaned_data['customer']
        quantity = request.POST['quantity']
        toppings = request.POST['toppings']
        description = request.POST['description']
        status = request.POST['status']

        if staff:
            order.staff = staff
        if product:
            order.product = product
        if customer:
            order.customer = customer
        if quantity:
            order.quantity = quantity
        if toppings:
            order.toppings = toppings
        if description:
            order.description = description
        if status:
            order.status = status

        order.save()
        messages.success(request, 'Order updated  successfully')
        return redirect('modify-order')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/auth')
def delete_order(request, id):
    if not request.user.is_staff:
        return redirect('products')
    order = Order.objects.get(pk=id)
    order.delete()
    messages.success(request, 'Order removed successfully')
    return redirect('modify-order')

# Delivery
@login_required(login_url='auth')
def create_delivery(request):
    if not request.user.is_staff:
        return redirect('products')
    if request.method == 'POST':
        forms = DeliveryForm(request.POST)
        context = {'form': forms}
        if not forms.is_valid():
            return render(request, 'dashboard/create_delivery.html', context)

        order = forms.cleaned_data['order']
        if order.status == 'complete':
            messages.error(request, "Can not deliver already delivered item")
            return render(request, 'dashboard/create_delivery.html', context)
        elif order.status == 'decline':
            messages.error(request, "Can not deliver declined item")
            return render(request, 'dashboard/create_delivery.html', context)

        order.status = "complete"
        order.save()
        forms.save()
        messages.success(request, "Order successfully delivered")
        return redirect('delivery-list')
    forms = DeliveryForm(request.GET)
    context = {
        'form': forms
    }
    return render(request, 'dashboard/create_delivery.html', context)


class DeliveryListView(ListView):
    model = Delivery
    template_name = 'dashboard/delivery_list.html'
    context_object_name = 'delivery'


@login_required(login_url='auth')
def order_summary(request):
    if request.method == 'GET':

        pendingOrder = Order.objects.filter(status__exact='pending').count()
        completeOrder = Order.objects.filter(status__exact='complete').count()
        declineOrder = Order.objects.filter(status__exact='decline').count()
        approvedOrder = Order.objects.filter(status__exact='approved').count()
        processingOrder = Order.objects.filter(status__exact='processing').count()

        baked_data = {}

        if pendingOrder:
            baked_data['PENDING'] = pendingOrder
        if approvedOrder:
            baked_data['APPROVED'] = approvedOrder
        if processingOrder:
            baked_data['PROCESSING'] = processingOrder
        if completeOrder:
            baked_data['COMPLETE'] = completeOrder
        if declineOrder:
            baked_data['DECLINED'] = declineOrder

        packaged_data = {'order_summary': baked_data}

        return JsonResponse(packaged_data, safe=False)
