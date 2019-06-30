from django.contrib import admin

from .models import Order, TGUser 

admin.site.register(Order)
admin.site.register(TGUser)