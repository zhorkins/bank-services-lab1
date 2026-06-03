from django.contrib import admin
from .models import BankService, BankRequest, BankServiceInRequest

from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(User, UserAdmin)

admin.site.register(BankService)
admin.site.register(BankRequest)
admin.site.register(BankServiceInRequest)

# Register your models here.
