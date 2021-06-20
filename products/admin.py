from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register([
    userlogindata,
    category,
    product,
    Cart,
    CartItems,
    OrderItem,
    Order,
    Address,
    payment,
    tips,
    parenting_tip
])