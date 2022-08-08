from unicodedata import category
from django.shortcuts import redirect, render,get_object_or_404
from django .contrib import messages,auth


from.models import Account
from . forms import  RegistrationForm
from django.contrib.auth import authenticate,logout 
from.otp import *
from product.models import *
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q
from cart.views import _cart_id
from cart.models import *
from category.models import Category
from django.contrib.auth.decorators import login_required
from orders.models import Order
from coupons.models import Coupon

def register(request):
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        print('form created')


        if form.is_valid():
            print('form valid')
            first_name = form.cleaned_data['first_name']
            last_name  = form.cleaned_data['last_name']
            email      = form.cleaned_data['email']
            gender     = form.cleaned_data['gender']
            mobile     = form.cleaned_data['mobile']
            password   = form.cleaned_data['password']

            print(first_name,last_name,email)

            user = Account.objects.create_user(
                first_name=first_name,
                last_name =last_name,
                email     =email,
                gender    =gender,
                mobile    =mobile,
                password  =password,
            )
        
            user.save()
            request.session['mobile']=mobile
            send_otp(mobile)
            print(mobile)
            return redirect('register_otp')

    form = RegistrationForm()
    context = { 'form' : form }
    return render(request,'signup.html',context)  

  



def user_login(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            user = Account.objects.get(email=email)
        except:
            messages.error(request,"user does not exist..")
            return redirect('login')
        if user.is_active:
            user = authenticate(request,email=email,password=password)
            if user is not None:
                auth.login(request,user)
                return redirect('home')
            else:
                messages.error(request,'user does not exit')

        else:
            messages.error(request,'you have been blocked by admin') 
            return redirect('login')   
    return render(request,'login.html')                

 



def home(request,category_slug=None):
    categories = None
    products =None
    coupons = Coupon.objects.all()
    if category_slug !=None:

        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories,available=True)
        paginator = Paginator(products, 4)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    else:


        products = Product.objects.all().filter(available=True)
        paginator = Paginator(products, 4)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
       
    context = {
        'products': paged_products,
        'coupons' : coupons,
    }
    return render(request,'index.html',context)





def otp_register(request):
    if request.method == 'POST':
        check_otp = request.POST.get('otp')
        print(check_otp)
        mobile=request.session['mobile']
        check=verify_otp(mobile,check_otp)
        if check:
            user = Account.objects.get(mobile = mobile)
            user.is_verified = True
            user.save()
            return redirect('home')
        else:
            messages.info(request,'Invalid OTP')
            return redirect('otp')
    return render(request,'register_otp.html')





def user_logout(request):
    auth.logout(request)
    return redirect('home')    





def search(request):
   
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by().filter(Q(description__icontains=keyword) | Q(name__icontains=keyword))
    context = {
        'products':products,
    }


    return render(request,'index.html',context)


@login_required(login_url='login')
def view_account(request):

    orders = Order.objects.filter(user=request.user)
    context={'orders':orders}
    return render(request,'view_account.html',context)