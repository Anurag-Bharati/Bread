from django import forms

from .models import Product, Order, Delivery


class StaffForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'name',
        'data-val': 'true',
        'data-val-required': 'Please enter name',
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'address',
        'data-val': 'true',
        'data-val-required': 'Please enter address',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'data-val': 'true',
        'data-val-required': 'Please enter email',
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'username',
        'data-val': 'true',
        'data-val-required': 'Please enter username',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'password',
        'data-val': 'true',
        'data-val-required': 'Please enter password',
    }))
    retype_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'retype_password',
        'data-val': 'true',
        'data-val-required': 'Please enter retype_password',
    }))


class CustomerForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'name',
        'data-val': 'true',
        'data-val-required': 'Please enter name',
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'address',
        'data-val': 'true',
        'data-val-required': 'Please enter address',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'data-val': 'true',
        'data-val-required': 'Please enter email',
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'username',
        'data-val': 'true',
        'data-val-required': 'Please enter username',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'password',
        'data-val': 'true',
        'data-val-required': 'Please enter password',
    }))
    retype_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'retype_password',
        'data-val': 'true',
        'data-val-required': 'Please enter retype_password',
    }))


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'type', 'price', 'desc']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),
            'type': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'type'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'price'
            }),
            'desc': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'desc'
            }),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'staff', 'product', 'quantity', 'toppings', 'description', 'customer',
        ]

        widgets = {
            'staff': forms.Select(attrs={
                'class': 'form-control', 'id': 'staff'
            }),
            'product': forms.Select(attrs={
                'class': 'form-control', 'id': 'product'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'quantity'
            }),
            'toppings': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'toppings'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'description'
            }),
            'customer': forms.Select(attrs={
                'class': 'form-control', 'id': 'customer'
            }),
        }

class EditOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'staff', 'product', 'quantity', 'toppings', 'description', 'customer', 'status',
        ]

        widgets = {
            'staff': forms.Select(attrs={
                'class': 'form-control', 'id': 'staff'
            }),
            'product': forms.Select(attrs={
                'class': 'form-control', 'id': 'product'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'quantity'
            }),
            'toppings': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'toppings'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'description'
            }),
            'customer': forms.Select(attrs={
                'class': 'form-control', 'id': 'customer'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control', 'id': 'status'
            }),
        }


class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = '__all__'

        widgets = {
            'order': forms.Select(attrs={
                'class': 'form-control', 'id': 'order'
            }),
            'staff': forms.Select(attrs={
                'class': 'form-control', 'id': 'staff'
            }),
            'order_name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'order_name'
            }),

        }
