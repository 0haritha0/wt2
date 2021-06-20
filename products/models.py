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
    quantity = models.IntegerField(default=20)
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


class Address(models.Model): 
    states = (
        ('AP', 'Andhra Pradesh'),
        ('KA', 'Karnataka'),
        ('TN', 'Tamil Nadu'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length = 10)
    locality = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)
    addr = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=20, choices = states)
    aphone =  models.CharField(max_length = 10)

    def __str__(self):
        return str(self.name) + " " + str(self.phone)


class payment(models.Model):
    payment_option =  models.CharField(max_length=50)
    def __str__(self):
        return self.payment_option


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE) 
    paymode = models.ForeignKey(payment, on_delete=models.CASCADE) 
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length = 10)
    address = models.CharField(max_length=150)
    total_price = models.FloatField(default=0)
    date_added = models.DateField(auto_now_add=True)
    time_added = models.TimeField(auto_now_add=True)
    order_id = models.CharField(max_length=150)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,null = True) 
    prod = models.ForeignKey(product,on_delete=models.CASCADE,null = True)
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=1)
    
class tips(models.Model):
    publish_status = (
        ('U', 'Unpublish'),
        ('P', 'Publish'),
    )
    author = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices = publish_status,null = True, default='Unpublish')
    def __str__(self):
        return self.title


class parenting_tip(models.Model):
    age_category = (
        ('1', '1-6 Months'),
        ('2', '1 year'),
        ('3', '1-2 years'),
        ('4', '2+ years'),
    )
    age = models.CharField(max_length=20, choices = age_category)
    tip_title =  models.CharField(max_length=200)
    tip_desc =  models.CharField(max_length=500)

    def __str__(self):
        return self.age+" - "+self.tip_title
    
    def get_ages(self):
        return self.age_category

    def get_age(self):
        return self.age
    

@receiver(pre_save, sender=CartItems)
def correct_price(sender, **kwargs):
    cart_items = kwargs['instance']
    price_of_product = product.objects.get(id=cart_items.prod.id)
    sp = price_of_product.get_discount_price()

    cart_items.price = float(cart_items.quantity) * sp
    total_cart_items = CartItems.objects.filter(user = cart_items.user )
    cart = Cart.objects.get(id = cart_items.cart.id)
    cart.save()
