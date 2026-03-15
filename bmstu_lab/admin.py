from django.contrib import admin

from bmstu_lab.models import Product, Order, ProductInOrder

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(ProductInOrder)

# Register your models here.
