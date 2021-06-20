from django.contrib import admin
from django.urls import path,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    
    path('',userhomepage,name = "homepage"),
    path('userloginpage/',userloginpage,name = "userloginpage"),
    path('userlogin/',userlogin,name="userlogin"),
    path('userhomepage/',userhomepage,name = "userhomepage"),
    path('userregister/',userregister,name = "userregister"),
    path("logout", logout_request, name= "logout"),
    path("register", register_request, name="register"),
    path('userhomepage/<int:category_id>/',product_list,name="product_list"),
    path('userhomepage/<int:category_id>/<int:product_id>/',product_details,name="product_details"),
    path('add/<int:proid>/',addtocart,name="addtocart"),
    path('usercart/<int:user_id>/',usercart,name="usercart"),
    path('cart/',cart,name="cart"),
    path('placeorder/',placeorder,name="placeorder"),
    path('orderoptions/',orderoptions,name="orderoptions"),
    path('myaddress/',myaddress,name="myaddress"),
    path('addaddress/',addaddress,name="addaddress"),
    path('deleteaddress/<int:addr_id>/',deleteaddress,name="deleteaddress"),
    path('usercart/delete/<int:cartid>/<int:cartiid>/',deletefromcart,name="delete"),
    path('myorders/',myorders,name="myorders"),
    path('ordersummary/<int:orderid>/',ordersummary,name="ordersummary"),
    path('blog/',blog,name="blog"),
    path('blog/<str:age_id>/',parenting,name="parenting"),
    
    path('publishedtips/',publishedtips,name="publishedtips"),
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)