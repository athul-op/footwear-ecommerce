from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages, auth
from product.forms import ProductForm
from account.models import Account
from product.models import *
from django.contrib.auth.decorators import login_required
from orders.models import Order     
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout


def master_signin(request):
    if request.user.is_authenticated and request.user.is_superadmin:
        return redirect("admin_home")

    if request.method == "POST":

        email = request.POST["email"]
        password = request.POST["password"]
        try:
            user = Account.objects.get(email=email, is_superadmin=True)
        except :
            messages.error(request,"admin does not exist")    
            return redirect("admin_signin")



        # email = request.POST["email"]
        # password = request.POST["password"]
        user = auth.authenticate(email=email,password=password,is_superadmin=True)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "Login Successful")
            return redirect("admin_home")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("admin_signin")

    else:
        return render(request, "admin_login.html")


@login_required(login_url='admin_signin')
def admin_home(request):
    if request.user.is_authenticated and request.user.is_superadmin:

        return render (request,'admin/admindash.html')
    else:
        return redirect("admin_home")

@login_required(login_url='admin_signin')
def customer(request):
    if request.user.is_authenticated and request.user.is_superadmin:
        users = Account.objects.all()
        context = {"users": users}
        return render(request, "admin/customer.html", context)
    else:
        return redirect("admin_home")

@login_required(login_url='admin_signin')
def customer_pickoff(request, customer_id):
    if request.user.is_authenticated and request.user.is_superadmin:
        customer = Account.objects.get(pk=customer_id)
        if customer.is_active:
            customer.is_active = False
            
        else:
            customer.is_active = True
        customer.save()

        return redirect("customer")
    else:
        return redirect("admin_home")


@login_required(login_url='admin_signin')
def add_product(request):
    if request.user.is_authenticated and request.user.is_superadmin:
        if request.method == "POST":
            form = ProductForm(request.POST,request.FILES)
            if form.is_valid():
                print('valid')
                form.save()
                print('data saved successfully')
                return redirect('add_product')
            else:
                print('product not added')
                messages.info(request,'product not added')
        else:
            form = ProductForm()
        return render(request,"add_product.html",{'form':form})
    else:
        return redirect("admin_home")


@login_required(login_url='admin_signin')
def view_product(request):
    if request.user.is_authenticated and request.user.is_superadmin:
        products = Product.objects.all()
        context = {"products": products}
        return render(request, "admin/view_edit.html", context)
    else:
        return redirect("admin_home")



def edit_product(request, id) :
    if request.user.is_authenticated and request.user.is_superadmin:
        product = Product.objects.get(id=id)
        if request.method == 'POST' :
            form = ProductForm(request.POST, request.FILES, instance=product)   
            if form.is_valid() :
                form.save()
                return redirect('view_product')
            
        form = ProductForm(instance=product)
        context = {'form' : form}
        return render(request,"admin/edit_product.html", context)
    else:
        return redirect("admin_home")


def delete_adminprod(request,id):
    if request.user.is_authenticated and request.user.is_superadmin:
        adminprod =  Product.objects.get(id=id)
        adminprod.delete()
        return redirect('view_product')
    else:
        return redirect("admin_home")


@never_cache
   
def admin_logouts(request):
    
    if request.user.is_superadmin:

        auth.logout(request)
        return redirect(master_signin)
    else:
        return redirect("admin_home")
    

@login_required(login_url='admin_signin')
def order_details(request):
    if request.user.is_authenticated and request.user.is_superadmin:
        order= Order.objects.all()
        context = {'order':order}
        return render(request,'admin/billing.html',context)
    else:
        return redirect("admin_home")

        

@login_required(login_url='admin_signin')
def edit_order(request,id):
    if request.user.is_authenticated and request.user.is_superadmin:
        order = Order.objects.get(id=id)
        if request.method =='POST':
            status = request.POST['status']

            order.status=status 
            order.save()
            print(order.status)
        return redirect('order_details')       
    else:
        return redirect("admin_home")