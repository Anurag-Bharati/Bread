from django.db import models

from users.models import User


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=220)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=220)
    profile_pic = models.ImageField(null=True, default="../default_customer.png")
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=120, unique=True)
    type = models.CharField(max_length=120, unique=False, null=True)
    price = models.PositiveSmallIntegerField(null=True)
    image = models.ImageField(null=True, default="../default_product.png")
    desc = models.CharField(max_length=200, unique=False, null=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICE = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('approved', 'Approved'),
        ('decline', 'Decline'),
        ('complete', 'Complete'),
    )
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(null=True)
    toppings = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.product.name + " by " + self.customer.name + " in " + self.created_date.__str__()


class Delivery(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_name = models.CharField(max_length=120)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.order_name
