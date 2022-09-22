
from base64 import urlsafe_b64decode
from itertools import count, product
import json
from multiprocessing import context
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from myApp import settings
from django.views.decorators.http import require_POST
from .tokens import generate_token
from .models import *



def root(request):
    return redirect(request.build_absolute_uri("/web"))
    
def index(request):
    return render(request,'index.html')


def home(request):
    return render(request,'home.html')

def products(request):
    return render(request,'products.html')

def product_view(request):
    return render(request,'product_view.html')

def contact(request):
    return render(request,'contact.html')

def search(request):
    return render(request,'search.html')

def vegetable(request):
    veg = Vegetable.objects.all()
    contex = {'veg':veg}
    context = {}
    return render(request,'vegetable.html',context)

def fruit(request):
    fru = Fruit.objects.all()
    context = {'fru':fru}
    return render(request,'fruit.html',context)

def oil(request):
    cook = Oil.objects.all()
    context = {'cook':cook}
    return render(request,'oil.html',context)

def snack(request):
    sna = Snack.objects.all()
    context = {'sna':sna}
    return render(request,'snack.html',context)

def spice(request):
    spy = Spice.objects.all()
    context = {'spy':spy}
    return render(request,'spice.html',context)

def legumes(request):
    legu = Legumes.objects.all()
    context = {'legu':legu}
    return render(request,'legumes.html',context)


def summary(request):
    if request.user.is_authenticated:
        customer = request.user
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items =[]
        order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False}
        cartItems = order['get_cart_items']

    context = {'items':items, 'order':order,'cartItems':cartItems}
    return render(request,'summary.html',context)

def item(request):
    if request.method == "POST":
        add_product_to_cart(request)
        
    cart_item_count = cart_count(request.user.id)
    request.user.cart_count = cart_item_count
    products = Product.objects.all()
    context = {'products':products}
    return render(request,'item.html',context)


def cart(request):
    if request.method == "POST":
        delete = request.POST.get('action') == "delete"
        modify_cart(request, delete)

    products = total_cost = 0
    
    if request.user.is_authenticated:
        customer = request.user.id
        items = Cart.objects.filter(user_id=customer).select_related()
        request.user.cart_count = cart_count(request.user.id)
        products = Cart.objects.filter(user_id=customer).count()
        total_cost = sum(item.total_cost for item in Cart.objects.filter(user_id=customer))
    else:
        items =[]
    context = {'items':items, 'products': products, 'total': total_cost}
    return render(request,'cart.html',context)



def main(request):
    context = {}
    return render(request,'main.html',context)

def allproducts(request):
    if request.method == "POST":
        add_product_to_cart(request)

    request.user.cart_count = cart_count(request.user.id)
    prod = All.objects.all()
    context = {'prod':prod}
    return render(request,'allproducts.html',context)
    
def packages(request):
    mix = Mixed.objects.all() 
    context = {'mix': mix}
    return render(request,'packages.html',context)



def signup(request):

    if request.method != "POST":
        return render(request,'signup.html')
    username = request.POST['username']
    fname = request.POST['fname']
    lname = request.POST['lname']
    email = request.POST['email']
    pas1 = request.POST['pas1']
    pas2 = request.POST['pas2']

    if User.objects.filter(username=username):
        messages.error(request ,"Username already exist! Please use other username")
        return redirect('signin')


    if User.objects.filter(email=email):
        messages.error(request, "Email  already exist! Please use other Email")
        return redirect('signin')

    if len(username)>10:
        messages.error(request,'Username must be under 10 charaters.')

    if pas1 != pas1 :
        messages.error(request,"Passwords didn't match!")

    if not username.isalnum():
        messages.error(request,'Username must be Alpha-numeric!')
        return redirect('signup')



    myuser = User.objects.create_user(username,email,pas1)
    myuser.first_name = fname
    myuser.last_name = lname
    myuser.is_active = False
    myuser.save()

    messages.success(request, 'Your Account has been successfully created.We have sent you aconfirmation email, Please confirm your email inorder to activate your account.')

    #welcome Email
    subject= "Welcome to oneshop = Django Login !!"
    message = f"Hello{myuser.first_name}" + "!! \n" + "Welcome to oneshop !! \n Thank you for Visiting our website \n We have also sent you a confirmation Email, Please confirm your Email Address in order to activate your Account.\n\n Thanking you."

    from_email = settings.EMAIL_HOST_USER
    to_list = [myuser.email]
    send_mail(subject, message, from_email, to_list, fail_silently = True)

    #Email Address comfirmation
    current_site = get_current_site(request)
    email_subject = "Confirm your email @oneshop-Django Login!!"
    message2 = render_to_string('email_confirmation.html',{
        'name':myuser.first_name,
        'domain':current_site.domain,
        'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
        'token': generate_token.make_token(myuser)

    })
    email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],

    )
    email.fail_silently = True
    email.send()

    return redirect('signin')


def signin(request):
    if request.user.is_authenticated:
        return redirect('/web/item')

    if request.method == "POST":

       username = request.POST['username']
       pas1 = request.POST['pas1']

       user = authenticate(username=username,password=pas1)
       
       if user is not None:
           login(request,user)
           return redirect('/web/item')

       else:
            messages.error(request,"Please enter a correct username and password. Try Again!")
            return redirect('signin')

    return render(request,'signin.html')

def signout(request):
    logout(request)
    messages.success(request,"Logged out Successful.")
    return redirect('index')


def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser=None

    if myuser is None or not generate_token.check_token(myuser, token):
        return render(request,'activation_fail.html')
    myuser.is_activate = True
    myuser.save()
    login(request,myuser)
    return redirect('home')

def updateCart(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('productId:', productId)


    customer = request.user
    product = Product.objects.get(id=productId)
    order,created = Order.objects.get_or_create(customer=customer,complete=False)
    orderItem,created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
      orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
       orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('it was added',safe=False)


#Add product to cart
def add_product_to_cart(request):
    product = int(request.POST.get('product'))
    price = int(float(request.POST.get('price')))
    user = request.user.id
    quantity = 1

    cart_item = Cart.objects.filter(product=product, user=user)

    if cart_item.exists():
        cart =  Cart.objects.get(product=product, user=user)
        quantity += cart.quantity
        cart.quantity = quantity
        cart.total_cost = quantity * price
        cart.save()
    else:
        cart_item = Cart.objects.create(product_id=product, total_cost=price, quantity=quantity, user_id=user)
        cart_item.save()   

    messages.success(request, "Product added to cart successully!")

def cart_count(user_id: str):
    return sum(item.quantity for item in Cart.objects.only('quantity').filter(user_id=user_id))

def modify_cart(request, delete=False):

    item_id = request.POST.get('id')
    if delete:
        Cart.objects.filter(id=item_id).delete()
        messages.success(request, "Product Item deleted from cart successully!")
    else:
        quantity = int(request.POST.get('quantity'))
        price = int(float(request.POST.get('price')))
        action = request.POST.get('action')
        
        actual_quantity = quantity + 1
        total_cost = price * actual_quantity
        if action == 'minus':
            total_cost = price * (quantity - 1)
            actual_quantity = quantity - 1
        
        cart = Cart.objects.filter(id=item_id).get()
        cart.quantity = actual_quantity
        cart.total_cost = total_cost
        cart.save()
        messages.success(request, f"Product Item modified successully! {action}")