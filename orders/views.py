from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Sum
from django.contrib import messages
from .models import Name_pizza,Regular_pizza,Sicilian_pizza,Topping,Sub_extra,Pasta,Salad,Dinner_platter,Order,User_order,Counter

counter = Counter.objects.first()
if counter==None:
    set_counter=Counter(counter=1)
    set_counter.save()
superuser = User.objects.filter(is_superuser=True)
if superuser.count() == 0:
    superuser=User.objects.create_user("admin","admin@admin.com","adminadmin")
    superuser.is_superuser = True
    superuser.is_staff = True
    superuser.save()
    set_superuser=User_order(user=superuser,order_number=counter.counter)
    set_superuser.save()

def index(request):
    if not request.user.is_authenticated:
        return render(request,"orders/login.html")
    order_number=User_order.objects.get(user=request.user,status='initiated').order_number
    context = {
        "user":request.user,
        "Checkout":Order.objects.filter(user=request.user,number=order_number),
        "Checkout_category":Order.objects.filter(user=request.user,number=order_number).values_list('category').distinct(),
        "Total":list(Order.objects.filter(user=request.user,number=order_number).aggregate(Sum('price')).values())[0],
        "Category": Name_pizza.objects.all(),
        "Order_number":order_number
    }
    return render(request,"orders/index.html",context)

def register(request):   #FALTA VERIFICAR EL NOMBRE DE USUARIO  
    if request.method == "POST":
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        if not password==password2:
            messages.warning(request, 'Passswords do not match, please try again.')
            return render(request,'orders/registration.html')
        user=User.objects.create_user(username, email, password)
        user.first_name=first_name
        user.last_name=last_name
        user.save()
        counter=Counter.objects.first()
        counter=Counter.objects.first()
        order_number=User_order(user=user,order_number=counter.counter)
        order_number.save()
        counter.counter=counter.counter+1
        counter.save()
        messages.success(request, f'{username}, your user has been created. Please, log in!')
        return render(request, 'orders/login.html')   
    return render(request,'orders/registration.html')

def login_u(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password) 
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.warning(request,'Invalid credentials, please try again')
            return render(request,"orders/login.html") 
    return render(request,"orders/login.html")     
    
def logout_u(request):
    logout(request)
    messages.warning(request,'Logged out.')
    return render(request,"orders/login.html")

def menu(request,category):
    menu,columns=Table(category)
    order_number=User_order.objects.get(user=request.user,status='initiated').order_number
    context = {
        "user":request.user,
        "Checkout":Order.objects.filter(user=request.user,number=order_number),
        "Checkout_category":Order.objects.filter(user=request.user,number=order_number).values_list('category').distinct(),
        "Total":list(Order.objects.filter(user=request.user,number=order_number).aggregate(Sum('price')).values())[0],
        "Category": Name_pizza.objects.all(),
        "Active_category":category,
        "Menu": menu,
        "Columns":columns,
        "Topping_price": 0.00,
        "Order_number":order_number
    }
    return render(request,"orders/menu.html",context)

def delete(request,category,name,price):
    menu,columns=Table(category)
    order_number=User_order.objects.get(user=request.user,status='initiated').order_number
    topping_allowance=User_order.objects.get(user=request.user,status='initiated')
    if (category == 'Regular Pizza' or category == 'Sicilian Pizza'):
        if name =="1 topping":
            topping_allowance.topping_allowance-=1
            topping_allowance.save()
        if name =="2 toppings":
            topping_allowance.topping_allowance-=2
            topping_allowance.save()
        if name =="3 toppings":
            topping_allowance.topping_allowance-=3    
            topping_allowance.save()
        topping_allowance.topping_allowance=0
        topping_allowance.save()
        delete_all_toppings=Order.objects.filter(user=request.user,category="Toppings")
        delete_all_toppings.delete()
    if category == "Toppings":
        topping_allowance.topping_allowance+=1
        topping_allowance.save()

    
    find_order=Order.objects.filter(user=request.user,category=category,name=name,price=price)[0]
    find_order.delete()                
    context = {
        "Checkout":Order.objects.filter(user=request.user,number=order_number),
        "Checkout_category":Order.objects.filter(user=request.user,number=order_number).values_list('category').distinct(),
        "Total":list(Order.objects.filter(user=request.user,number=order_number).aggregate(Sum('price')).values())[0],
        "user":request.user,
        "Category": Name_pizza.objects.all(),
        "Active_category":category,
        "Menu": menu,
        "Columns":columns,
        "Topping_price": 0.00,
        "Order_number":order_number
    }
    return render(request,"orders/menu.html",context)

def user_orders(request,order_number):
    context = {
        "Checkout":Order.objects.filter(user=request.user,number=order_number),
        "Checkout_category":Order.objects.filter(user=request.user,number=order_number).values_list('category').distinct(),
        "Total":list(Order.objects.filter(user=request.user,number=order_number).aggregate(Sum('price')).values())[0],
        "user":request.user,
        "Category": Name_pizza.objects.all(),
        "Order_number":order_number,
        "All_orders":User_order.objects.filter(user=request.user),
        "Status":User_order.objects.get(user=request.user,order_number=order_number).status
    }
    return render(request,"orders/user_order.html",context)

def confirmed(request,order_number):
    status=User_order.objects.get(user=request.user,status='initiated')
    status.status='pending'
    status.save()

    counter=Counter.objects.first()
    new_order_number=User_order(user=request.user,order_number=counter.counter)
    new_order_number.save()
    counter.counter=counter.counter+1
    counter.save()
    
    return user_orders(request,order_number)

def Table(category):
    if category == "Regular Pizza":
        menu=Regular_pizza.objects.all()
        columns=3
    elif category == "Sicilian Pizza":
        menu=Sicilian_pizza.objects.all()
        columns=3
    elif category == "Toppings":
        menu=Topping.objects.all()
        columns=1
    elif category == "Salad":
        menu=Salad.objects.all()
        columns=2
    elif category == "Subs":
        menu=Sub_extra.objects.all()
        columns=3
    elif category == "Pasta":
        menu=Pasta.objects.all()
        columns=2
    elif category == "Dinner Platters":
        menu=Dinner_platter.objects.all()
        columns=3
    return menu,columns 

def add(request,category,name,price):
    menu,columns=Table(category)
    order_number=User_order.objects.get(user=request.user,status='initiated').order_number
    topping_allowance=User_order.objects.get(user=request.user,status='initiated')
    context = {
        "Checkout":Order.objects.filter(user=request.user,number=order_number),
        "Checkout_category":Order.objects.filter(user=request.user,number=order_number).values_list('category').distinct(),
        "Total":list(Order.objects.filter(user=request.user,number=order_number).aggregate(Sum('price')).values())[0],
        "user":request.user,
        "Category": Name_pizza.objects.all(),
        "Active_category":category,
        "Menu": menu,
        "Columns":columns,
        "Topping_price": 0.00,
        "Order_number":order_number
    }
    if (category == 'Regular Pizza' or category == 'Sicilian Pizza'):
        if name =="1 topping":
            topping_allowance.topping_allowance+=1
            topping_allowance.save()
        if name =="2 toppings":
            topping_allowance.topping_allowance+=2
            topping_allowance.save()
        if name =="3 toppings":
            topping_allowance.topping_allowance+=3    
            topping_allowance.save()
    if category == "Toppings" and topping_allowance.topping_allowance == 0:
        return render(request,"orders/menu.html",context) 
    if category == "Toppings" and topping_allowance.topping_allowance > 0:
        topping_allowance.topping_allowance-=1
        topping_allowance.save()

    add=Order(user=request.user,number=order_number,category=category,name=name,price=price) 
    add.save()      
    context2 = {
        "Checkout":Order.objects.filter(user=request.user,number=order_number),
        "Checkout_category":Order.objects.filter(user=request.user,number=order_number).values_list('category').distinct(),
        "Total":list(Order.objects.filter(user=request.user,number=order_number).aggregate(Sum('price')).values())[0],
        "user":request.user,
        "Category": Name_pizza.objects.all(),
        "Active_category":category,
        "Menu": menu,
        "Columns":columns,
        "Topping_price": 0.00,
        "Order_number":order_number
    }       
    return render(request,"orders/menu.html",context2)

def admin_orders(request,user,order_number):
    user=User.objects.get(username=user)
    context = {
        "Checkout":Order.objects.filter(user=user,number=order_number),
        "Checkout_category":Order.objects.filter(user=user,number=order_number).values_list('category').distinct(),
        "Total":list(Order.objects.filter(user=user,number=order_number).aggregate(Sum('price')).values())[0],
        "user":request.user,
        "Category": Name_pizza.objects.all(),
        "Order_number":order_number,
        "All_orders":User_order.objects.exclude(status='initiated')
    }
    return render(request,"orders/admin_order.html",context)


def complete_order(request,user,order_number):
    user=User.objects.get(username=user)
    complete=User_order.objects.get(user=user,order_number=order_number)
    complete.status='completed'
    complete.save()

    context = {
        "Checkout":Order.objects.filter(user=user,number=order_number),
        "Checkout_category":Order.objects.filter(user=user,number=order_number).values_list('category').distinct(),
        "Total":list(Order.objects.filter(user=user,number=order_number).aggregate(Sum('price')).values())[0],
        "user":request.user,
        "Category": Name_pizza.objects.all(),
        "Order_number":order_number,
        "All_orders":User_order.objects.exclude(status='initiated')
    }
    return render(request,"orders/admin_order.html",context)