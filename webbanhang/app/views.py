from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.http import HttpResponse,JsonResponse
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages

# Create your views here.
def search(request):
    if request.method == "POST":
        reseached = request.POST['reseached']
        keys = Product.objects.filter(name__contains = reseached)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    
    products = Product.objects.all()
    return render(request,'app/search.html',{"reseached":reseached,"keys":keys,'products':products,'cartItems':cartItems,"user_not_login":user_not_login,"user_login":user_login})
def register(request):
    form = CreateUserForm()
    user_not_login = "show"
    user_login = "hidden"
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form':form,"user_not_login":user_not_login,"user_login":user_login}

    return render(request,'app/register.html',context)
def loginPage(request):
    user_not_login = "show"
    user_login = "hidden"
    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = "show"
        return redirect('home',{"user_not_login":user_not_login,"user_login":user_login})
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        user_not_login = "hidden"
        user_login = "show"
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'user or password not correct')
                
    context = {"user_not_login":user_not_login,"user_login":user_login}
    return render(request,'app/login.html',context)
def logoutPage(request):
    logout(request)
    return redirect('login')
def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    products = Product.objects.all()
    context = {'products':products,'cartItems':cartItems,"user_not_login":user_not_login,"user_login":user_login}
    return render(request,'app/home.html',context)
# Create your views here.
def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    context = {"items": items,"order":order,'cartItems':cartItems,"user_not_login":user_not_login,"user_login":user_login}
    return render(request,'app/cart.html',context)
def detail(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer,complete=True)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    id = request.GET.get('id','')
    product = Product.objects.filter(id=id)
    context = {"product":product,"items": items,"order":order,'cartItems':cartItems,"user_not_login":user_not_login,"user_login":user_login}
    return render(request,'app/detail.html',context)
# Create your views here.
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer,complete=False)

        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
        if request.method == 'POST':
            address = request.POST.get('address')
            cyti = request.POST.get('city')
            state = request.POST.get('state')
            mobile = request.POST.get('mobile')
            country = request.POST.get('country')
            name = request.POST.get('name')
            order, created = ShippingAddress.objects.get_or_create(customer=customer,order=order,address=address,cyti=cyti,state=state,mobile=mobile)

    else:
        items = []
        order = {'get_cart_items':0,'get_cart_total':0}
        user_not_login = "show"
        user_login = "hidden"
    context = {"items": items,"order":order,'cartItems':cartItems,"user_not_login":user_not_login,"user_login":user_login}
    return render(request,'app/checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer,complete=False)
    orderItem, created = OrderItem.objects.get_or_create(customer=customer,order=order,product=product)

    if action == 'add':
        orderItem.quantity +=1
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()
    if orderItem.quantity <=0:
        orderItem.delete()

    return JsonResponse('added',safe=False)