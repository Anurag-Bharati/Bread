import threading
import validate_email as EmailValidator

from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.cache import cache_control
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from bread import settings
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
    paginate_by = 1
    ordering = 'id'


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
    paginate_by = 1
    ordering = 'id'


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
    ordering = '-id'
    paginate_by = 1


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
    paginate_by = 1
    context_object_name = 'order'
    ordering = '-id'


class ModifyOrder(ListView):
    model = Order
    template_name = 'dashboard/modify_order.html'
    paginate_by = 1
    context_object_name = 'order'
    ordering = '-id'


class ModifyProduct(ListView):
    model = Product
    template_name = 'dashboard/modify_product.html'
    paginate_by = 1
    context_object_name = 'products'
    ordering = '-id'


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
            if order.status == 'decline' and EmailValidator.validate_email(str(order.customer.user.email).lower()):
                remarks = "Unavailable"
                email_context = render_to_string('email/order_declined.html',
                                                 {'user': customer.user.username, "product": product.name,
                                                  'type': product.type,
                                                  "staff": staff.name, "remarks": remarks, })
                text_content = strip_tags(email_context)

                mail = EmailMultiAlternatives(
                    "Order Rejected ❌",
                    text_content,
                    settings.EMAIL_HOST_USER,
                    [str(customer.user.email).lower()],
                )
                mail.attach_alternative(email_context, "text/html")

                Thread(mail).start()

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


@login_required(login_url='/auth')
def edit_product(request, id):
    if not request.user.is_staff:
        return redirect('products')
    product = Product.objects.get(pk=id)
    if request.method == 'GET':
        forms = ProductForm(initial={
            'name': product.name,
            'type': product.type,
            'price': product.price,
            'desc': product.desc,
            'image': product.image.url,
            'is_featured': product.is_featured,
            'is_special': product.is_special,
        })
        context = {
            'form': forms
        }
        return render(request, 'dashboard/edit-product.html', context)

    elif request.method == 'POST':
        forms = ProductForm(request.POST, request.FILES)
        if not forms.is_valid():
            context = {'form': forms}
            messages.error(request, 'Please, Provide valid form data')
            return render(request, 'dashboard/edit-product.html', context)

        name = request.POST['name']
        if name and not product.name == name:
            product.name = name

        type = request.POST['type']
        if type and product.type != type:
            product.type = type

        price = request.POST['price']
        if price and product.price != price:
            product.price = price

        desc = request.POST['desc']
        if desc and product.desc != desc:
            product.desc = desc

        image = request.FILES.get('image', None)

        if image and product.image.name != image.name:
            product.image = image

        is_featured = request.POST['is_featured']
        if is_featured and product.is_featured != is_featured:
            if is_featured == 'true':
                product.is_featured = True
            else:
                product.is_featured = False

        is_special = request.POST['is_special']
        if is_special and product.is_special != is_special:
            if is_special == 'true':
                product.is_special = True
            else:
                product.is_special = False

        product.save()
        messages.success(request, 'Product updated  successfully')
        return redirect('modify-product')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/auth')
def delete_product(request, id):
    if not request.user.is_staff:
        return redirect('products')
    product = Product.objects.get(pk=id)
    product.delete()
    messages.success(request, 'Product removed successfully')
    return redirect('modify-product')


# Delivery
@login_required(login_url='auth')
def create_delivery(request):
    if not request.user.is_staff:
        return redirect('products')
    if request.method == 'POST':
        forms = DeliveryForm(request.POST)
        context = {'form': forms}
        if not forms.is_valid():
            messages.error(request, 'Please, Provide valid form data')
            return render(request, 'dashboard/create_delivery.html', context)

        order = forms.cleaned_data['order']

        if order.status == 'complete':
            messages.error(request, "Can not deliver already delivered item")
            return render(request, 'dashboard/create_delivery.html', context)
        elif order.status == 'decline':
            messages.error(request, "Can not deliver declined item")
            return render(request, 'dashboard/create_delivery.html', context)
        staff = Staff.objects.get(id=request.POST['staff'])
        order.status = "complete"
        delivery = Delivery()
        delivery.order = forms.cleaned_data['order']
        delivery.staff = forms.cleaned_data['staff']
        remarks = ""
        if request.POST['remarks']:
            delivery.remarks = request.POST['remarks']
            remarks = delivery.remarks
        else:
            remarks = "None"
        delivery.save()
        order.save()
        if EmailValidator.validate_email(str(order.customer.user.email).lower()):
            email_context = render_to_string('email/order_ready.html',
                                             {'user': order.customer.user.username, "product": order.product.name,
                                              'type': order.product.type,
                                              "staff": staff.name, "token": delivery.token, "remarks": remarks, })
            text_content = strip_tags(email_context)

            mail = EmailMultiAlternatives(
                "Collect your order 📦",
                text_content,
                settings.EMAIL_HOST_USER,
                [str(order.customer.user.email).lower()],
            )
            mail.attach_alternative(email_context, "text/html")

            Thread(mail).start()
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
    paginate_by = 1
    ordering = '-id'


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


class Thread(threading.Thread):

    def __init__(self, task):
        self.task = task
        threading.Thread.__init__(self)

    def run(self):
        self.task.send(fail_silently=False)
