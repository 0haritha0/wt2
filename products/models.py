from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver

# Create your models here.
class userlogindata(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.user.username

class category(models.Model):
    category_name = models.CharField(max_length=50)
    category_desc = models.CharField(max_length=150)
    category_image = models.ImageField(null = True)
    
    def __str__(self):
        return self.category_name

class product(models.Model):
    product_brand = models.CharField(max_length=50)    
    product_name = models.CharField(max_length=150)
    product_price = models.FloatField()
    product_discount = models.FloatField(default=0)
    product_fprice = models.FloatField(default=0)
    product_image = models.ImageField()
    product_category = models.ForeignKey(category, on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.product_brand + " - " + self.product_name
    
    def get_discount_price(self):
        d = self.product_discount
        l = self.product_price
        s = l * ( (100 - d) / 100)
        s= round(s)
        return s

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    total_price = models.FloatField(default=0)

    def __str__(self):
        return str(self.user.username) + " " + str(self.total_price)

class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prod = models.ForeignKey(product,on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return str(self.user.username) + " " + str(self.prod.product_name)


@receiver(pre_save, sender=CartItems)
def correct_price(sender, **kwargs):
    cart_items = kwargs['instance']
    price_of_product = product.objects.get(id=cart_items.prod.id)
    sp = price_of_product.get_discount_price()

    cart_items.price = float(cart_items.quantity) * sp
    total_cart_items = CartItems.objects.filter(user = cart_items.user )
    cart = Cart.objects.get(id = cart_items.cart.id)
    cart.save()