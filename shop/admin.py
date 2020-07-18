from django.contrib import admin

# Register your models here.
from .models import Product, Contact , Order123,Orderupdate

admin.site.register(Product)
admin.site.register(Contact)

admin.site.register(Order123)
admin.site.register(Orderupdate)