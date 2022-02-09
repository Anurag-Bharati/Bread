from django.contrib import admin
from .models import Staff, Customer, Product, Order, Delivery


class StaffAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'address', 'created_date']


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'address', 'created_date']


admin.site.register(Staff, StaffAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Delivery)
