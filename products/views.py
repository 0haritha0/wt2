from django.shortcuts import render

# Create your views here.

from django.shortcuts import render,redirect
from django import forms
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import *
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
import datetime
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated


'''
def homepageview(request):
    html = "<html><body>This is home page</body></html>"
    return HttpResponse(html)
'''

def homepageview(request):
    categories = category.objects.all()
    context = {'categories' : categories,'username' : request.user.username}
    return render(request,"products/home.html",context)


def userloginpage(request):
    return render(request,"products/login.html")

def userlogin(request):
    username = request.POST['username']
    password = request.POST['password']
    try:
        User.objects.filter(username = username)[0]
    except:
        messages.add_message(request, messages.INFO, "invalid credentials ! check username and password")
        return redirect("userloginpage")

    user = authenticate(username = username,password = password)

    if user is not None:
        login(request,user)
        return redirect("userhomepage")
    messages.add_message(request, messages.INFO, "invalid credentials ! check username and password")
    return redirect(request.META["HTTP_REFERER"])


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("main:homepage")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="main/login.html", context={"login_form":form})

def userhomepage(request):
    categories = category.objects.all()
    context = {'categories' : categories,'username' : request.user.username}
    return render(request,"products/home.html",context)


def taskval(request):
    task=request.POST['username']
    loc=request.POST['password']
    d=request.POST['date']
    t=request.POST['time']
    user=userlogindata.objects.filter(user=request.user)[0]
    messages.info(request,"Task Added successfully")
    return redirect("userhomepage")


def userregister(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('userhomepage')
    return render(request, 'products/register.html', {'form': form})
    #return render(request, 'products/register.html', {'form': f})


def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("userloginpage")

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user


def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
            
			return redirect("userhomepage")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm
	return render (request=request, template_name="products/register1.html", context={"register_form":form})


def product_list(request,category_id):
    cat = category.objects.get(pk=category_id)
    product_list = product.objects.filter(product_category = cat)
    context = {'category_id' : category_id ,'product_list' : product_list, 'cat' : cat}
    return render(request,'products/product_list.html',context)


def product_details(request, category_id, product_id):
    cat = category.objects.get(pk=category_id)
    pro = product.objects.get(pk=product_id)
    
    u= request.user
    product_list = product.objects.filter(product_category = cat)
    context = {'category_id' : category_id ,'product_list' : product_list, 'cat' : cat, 'pro' : pro,'u':u }
    return render(request,'products/product_page.html',context)


def addtocart(request,proid):
    # get quantity
    quentity = request.POST['quantity']
    # check product
    prods = product.objects.get(id = proid)
    # get user
    cuser = request.user

    cat_id = prods.product_category.id

    #check for cart existence
    carts = Cart.objects.filter(user = cuser)
    b=carts.count()

    if prods.quantity <= 0:
        messages.add_message(request,messages.INFO,'Item out of stock!')
        return redirect('product_details',cat_id,proid)
    
    if float(quentity) < 1.0:
        messages.add_message(request,messages.INFO,'Minimum quantity should be 1')
        return redirect('product_details',cat_id,proid)
    
    if prods.quantity-float(quentity) < 0:
        messages.add_message(request,messages.INFO,'Only '+str(prods.quantity)+' items left!')
        return redirect('product_details',cat_id,proid)
        
    if b==0:
        Cart.objects.create(user=cuser).save()

    
    carts = Cart.objects.get(user = cuser)
    
    #add items to cart
    #check if the item already exists in the cart
    carti = CartItems.objects.filter(cart=carts).filter(prod=prods)
    c = carti.count()

    if c==0:
        CartItems.objects.create(user=cuser,cart=carts,prod=prods,quantity=quentity).save()
    else :
        carti = CartItems.objects.get(cart=carts,prod=prods)
        carti.quantity = quentity
        carti.save()

    carti = CartItems.objects.get(cart=carts,prod=prods)
    
    carti_list = CartItems.objects.filter(cart=carts).aggregate(Sum('price'))

    carts.total_price =  carti_list['price__sum']
    carts.save()
    messages.add_message(request,messages.INFO,'Item added to cart')
    return redirect('cart')


def usercart(request, user_id):
    cuser = User.objects.get(id = user_id)
    usercart = Cart.objects.get(user=cuser)
    items = CartItems.objects.filter(cart = usercart)
    total = CartItems.objects.filter(cart = usercart).aggregate(Sum('quantity'))
    context = {'items' : items,'username' : request.user.username, 'usercart' :usercart,'total':total}
    return render(request,"products/cart.html",context)

def deletefromcart(request,cartid,cartiid):
    c = Cart.objects.get(id = cartid)
    item = CartItems.objects.get(id = cartiid)
    c.total_price = c.total_price - item.price
    c.save()
    CartItems.objects.get(id = cartiid).delete()
    return redirect(request.META['HTTP_REFERER'])

def cart(request):
    user_id = request.user.id
    cuser = User.objects.get(id = user_id)

    carts = Cart.objects.filter(user = cuser)
    b=carts.count()
    if b==0:
        Cart.objects.create(user=cuser).save()

    usercart = Cart.objects.get(user=cuser)
    items = CartItems.objects.filter(cart = usercart)
    total = CartItems.objects.filter(cart = usercart).aggregate(Sum('quantity'))
    context = {'items' : items,'username' : request.user.username, 'usercart' :usercart,'total':total}
    return render(request,"products/cart.html",context)

def orderoptions(request):
    user_id = request.user.id
    cuser = User.objects.get(id = user_id)

    carts = Cart.objects.filter(user = cuser)
    b=carts.count()
    if b==0:
        Cart.objects.create(user=cuser).save()

    usercart = Cart.objects.get(user=cuser)
    items = CartItems.objects.filter(cart = usercart)
    total = CartItems.objects.filter(cart = usercart).aggregate(Sum('quantity'))
    addresses = Address.objects.filter(user = cuser)
    payments = payment.objects.all()
    context = {'items' : items, 'usercart' :usercart,'total':total,'addresses':addresses,'payments':payments}
    return render(request,"products/address_options.html",context)

def placeorder(request):
    
    address_id = request.POST['addr']
    payment_id = request.POST['pay']
    address = Address.objects.get(pk=address_id)
    pay = payment.objects.get(pk=payment_id)
    cuser = request.user
    usercart = Cart.objects.get(user = cuser)
    atime = datetime.datetime.now()
    adate = datetime.datetime.now()
    price = usercart.total_price
    orderid = "BW-"+str(adate.year)+str(adate.month)+str(adate.day)+"-"+str(adate.hour)+str(adate.minute)+str(adate.second)
    name = address.name
    phone = address.phone
    addr = address.addr+", "+ address.locality+", "+address.city+", "+address.state+" "+address.pincode
    Order.objects.create(cart=usercart,total_price=price,date_added=atime,time_added=adate,order_id=orderid,address=addr,paymode=pay,name=name,phone=phone).save()
    userorder =  Order.objects.get(order_id=orderid)
    items = CartItems.objects.filter(cart = usercart)
    i = []
    for item in items:
        OrderItem.objects.create(order=userorder,prod=item.prod,price=item.price,quantity=item.quantity).save()
        product = item.prod
        product.quantity = product.quantity - item.quantity
        product.save()
        i.append(item.prod)
    
    orderitems = OrderItem.objects.filter(order = userorder)
    context ={'userorder':userorder,'address':address,'orderitems':orderitems}
    items.delete()

    return render(request,"products/ordered.html",context)

def myaddress(request):
    cuser = request.user
    addresses = Address.objects.filter(user = cuser)
    states = addresses.__getstate__
    context = {'addresses' : addresses,'states':states}
    return render(request,"products/myaddress.html",context)

def addaddress(request):
    cuser = request.user
    name = request.POST['name']
    phoneno = request.POST['phoneno']
    pincode = request.POST['pincode']
    locality = request.POST['locality']
    address = request.POST['address']
    city = request.POST['city']
    value = request.POST['state']
    landmark = request.POST['landmark']
    aphone = request.POST['aphone']
    Address.objects.create(user=cuser,name=name,phone=phoneno,locality=locality,addr=address,city=city,state=landmark,aphone=aphone,pincode=pincode).save()
    context = {'value' : value}
    return redirect('myaddress')
    #return render(request,"products/sample.html",context)

def deleteaddress(request,addr_id):
    cuser = request.user
    addr = Address.objects.get(id = addr_id)
    addr.delete()
    return redirect('myaddress')

def myorders(request):
    cuser = request.user
    usercart = Cart.objects.get(user = cuser)
    orders = Order.objects.filter(cart = usercart)

    context = {'orders':orders}
    return render(request,"products/myorders.html",context)

def ordersummary(request, orderid):

    userorder =  Order.objects.get(pk = orderid)
    orderitems = OrderItem.objects.filter(order = userorder)
    context ={'userorder':userorder,'orderitems':orderitems}

    return render(request,"products/ordered.html",context)

def blog(request):
    all_tips = tips.objects.all()
    tip_l = tips.objects.filter(status = 'P').last()
    tips_p = parenting_tip.objects.all().last()
    ages = tips_p.get_ages()
    age = ages[0][1]
    context ={'all_tips':all_tips,'tips_p':tips_p,'tip_l':tip_l,'ages':ages,'age':age}

    return render(request,"products/tips.html",context)

def parenting(request,age_id):
    age_tips = parenting_tip.objects.filter(age = age_id)
    aget = age_tips.last()
    aget = aget.get_age_display()
    context ={'age_tips':age_tips,'aget':aget}

    return render(request,"products/age_tips.html",context)

def publishedtips(request):
    
    tips_all = tips.objects.filter(status = 'P').reverse()
    context ={'all_tips':tips_all}

    return render(request,"products/publishedtips.html",context)