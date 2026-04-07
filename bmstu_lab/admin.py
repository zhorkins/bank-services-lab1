from django.contrib import admin
from .models import BankService, BankRequest, BankServiceInRequest

admin.site.register(BankService)
admin.site.register(BankRequest)
admin.site.register(BankServiceInRequest)

# Register your models here.
