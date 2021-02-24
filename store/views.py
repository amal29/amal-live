from django.shortcuts import render,redirect
from .models import *
from django.http import JsonResponse
import json
import datetime 
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string


def Login(request):
    if request.method =='POST':
        username=  request.POST.get('username')
        password= request.POST.get('password')
        user=authenticate(request,username=username,password=password)
       
        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.info(request,'Username or Password is Incorrect')

    return render(request,'login.html')


def Logout(request):
    logout(request)
    return redirect('login')


def Register(request):
    form=CreateUserForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user=form.cleaned_data.get('username')
            messages.success(request,'Account was created for ' +  user)
            return redirect('login')
    context={'form':form}
    return render(request,'register.html',context)


def Search(request):
    search = request.GET.get("ser_itm")
    print("SEARCHITEM:",search)
    itm=Product.objects.filter(name__contains=search)  
    if request.user.is_authenticated:
        customer = request.user
        print(customer)
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems=order.get_cart_items
       
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False}
        cartItems= order['get_cart_items']
    
    html_data=render_to_string('text.html',{'products':itm,'cartItems':cartItems},request=request)
    print("html_data")
    # return render(request,'search.html',{'products':itm,'cartItems':cartItems}) 
    return JsonResponse({'html_data':html_data})






def store(request):
    if request.user.is_authenticated:
        customer = request.user
        print(customer)
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems=order.get_cart_items
       
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False}
        cartItems= order['get_cart_items']
    products= Product.objects.all()
    context=json.dumps(list(Product.objects.values()))
    return render(request,'store.html',{"products":products,'cartItems':cartItems,'context':context})



def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems=order.get_cart_items
        
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False}
        cartItems= order['get_cart_items']

    context = {'items':items,'cartItems':cartItems,'order':order}
    return render(request,'cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems=order.get_cart_items

    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False}
        cartItems= order['get_cart_items']

    context = {'items':items,'order':order,'cartItems':cartItems}
    
    return render(request,'checkout.html',context)

def main(request):
    return render(request,'main.html')

@login_required(login_url='login')
def updateItem(request):
     data = request.GET.get('productId')
     action = request.GET.get('action')
     print(action)
    #  data=str(data)

     print(data)

     customer=request.user
     product=Product.objects.get(id=data)
     print("product:",product)

     order,created = Order.objects.get_or_create(customer=customer,complete=False)
     orderItem,created = OrderItem.objects.get_or_create(order=order,product=product)
    #  ob=OrderItem.objects.all()
    #  for i in ob:
     print("orderItem.quantity",orderItem.quantity) 

     if action == 'add':
         orderItem.quantity= (orderItem.quantity +1)

     elif action == 'remove':
         orderItem.quantity=(orderItem.quantity -1)
     orderItem.save()
     if orderItem.quantity <=0:
         orderItem.delete()

     return JsonResponse('Item  is Added', safe=False)
   


def processOrder(request):
    transation_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)
    if request.user.is_authenticated:
        customer=request.user
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        total=float(data['form']['total'] )
        order.transation_id=transation_id

        if total == order.get_cart_total:
            order.complete=True
        order.save()    

        if order.shipping==True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                state=data['shipping']['state'],
                city=data['shipping']['city'],
                zipcode=data['shipping']['zipcode'],


            )
    else:
        print("User is not Logged in ...")    
    return JsonResponse('Payment Complete!', safe=False)

