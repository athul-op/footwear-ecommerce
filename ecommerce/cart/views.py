
from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, redirect, render

from product.models import Product
from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .models import Wishlist,WishlistItem
from django .contrib import messages
from coupons.models import Coupon,CouponUsers
# Create your views here.




def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request,product_id):
    current_user =request.user
    product = Product.objects.get(id=product_id)

    if current_user.is_authenticated:
        
        try:
            cart_item =CartItem.objects.get(product=product,user=current_user)
            cart_item.quantity += 1
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item =CartItem.objects.create(
            product=product,
            quantity =1,
            user =current_user,
        ) 
            cart_item.save()
    
        return redirect('cart')  
    #if user is not authenticated
    else:


        try:
            cart =Cart.objects.get(cart_id=_cart_id(request))

        except Cart.DoesNotExist:


            cart =Cart.objects.create(
            cart_id = _cart_id(request)
        )
        cart.save()


        try:
            cart_item =CartItem.objects.get(product=product,cart=cart)
            cart_item.quantity += 1
            cart_item.save()

        except CartItem.DoesNotExist:

            cart_item =CartItem.objects.create(
            product=product,
            quantity =1,
            cart =cart,
        ) 
            cart_item.save()
    
        return redirect('cart')      

    

def remove_cart(request,product_id):
    
    product = get_object_or_404(Product,id=product_id)
    
    try:
       if request.user.is_authenticated:

           cart_item= CartItem.objects.get(product=product,user=request.user)

       else:
           cart =Cart.objects.get(cart_id=_cart_id(request))

           cart_item= CartItem.objects.get(product=product,cart=cart)
       if cart_item.quantity >1:

          cart_item.quantity -=1
          cart_item.save()

       else:

           cart_item.delete()    

    except:
        pass
    
    return redirect('cart') 


def remove_item_fully(request,product_id):
    current_user = request.user
    product = get_object_or_404(Product,id=product_id)

    if request.user.is_authenticated:

        cart_item =CartItem.objects.get(product=product,user=current_user)  

    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))  
        cart_item= CartItem.objects.get(product=product,cart=cart)

    cart_item.delete()

    return redirect('cart')

def test(request):
    return render(request,'test.html')

    
@login_required(login_url='login')
def add_coupon(request):
    coupon=0
    if request.method == 'POST':
        code = request.POST['code']

        if Coupon.objects.filter(coupon_code=code, is_available=True).exists() and  CouponUsers.objects.filter(user= request.user, coupon__coupon_code=code ).exists() == False :
            coupon_object = Coupon.objects.get(coupon_code=code, is_available=True)
            coupon_user = CouponUsers()
            coupon_user.user    = request.user
            coupon_user.coupon  = coupon_object
            coupon_user.is_used = False
            coupon_user.amount  = coupon_object.amount
            coupon_user.save()

            coupon_object.quantity -= 1
            if coupon_object.quantity == 0:
                coupon_object.is_available = False
            coupon_object.save()    
            
    return redirect(cart)




def cart(request,total=0,quantity=0, coupon=0,cart_items=None):
   
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)


            if CouponUsers.objects.filter(user=request.user, is_used= False).exists():
                coupon_user = CouponUsers.objects.get(user=request.user,is_used= False)
                coupon      = coupon_user.amount



        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total +=(cart_item.product.price * cart_item.quantity)
            quantity +=cart_item.quantity

        # if CouponUsers.objects.filter(user=request.user, is_used= False).exists() :
        #     coupon_user = CouponUsers.objects.get(user=request.user, is_used= False)
        #     coupon      = coupon_user.amount
        tax = (3 * total)/100
        grand_total = total + tax - coupon
    except ObjectDoesNotExist:
        pass      



    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax'       :tax,
        'grand_total':grand_total,
        'coupon'     :coupon,
    }  
    return render(request,'cart.html',context)


@login_required(login_url='login')
def checkout(request,total=0,quantity=0,coupon=0,cart_items=None):
    try:
        tax=0
        grand_total=0 
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)


        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,is_active=True)

    
        
        for cart_item in cart_items:
            if cart_item.product.stock < cart_item.quantity :
                messages.error(request, f'There is no enough stock of {cart_item.product.name} !!!')
                return redirect('cart')
            else :
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
            # total +=(cart_item.product.price * cart_item.quantity)
            # quantity +=cart_item.quantity

        if CouponUsers.objects.filter(user=request.user, is_used= False).exists() :
            coupon_user = CouponUsers.objects.get(user=request.user, is_used= False)
            coupon      = coupon_user.amount


        tax = (3 * total)/100
        grand_total = total + tax -coupon
    except ObjectDoesNotExist:
        pass      

    


    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax'       :tax,
        'grand_total':grand_total,
        'coupon'      : coupon
    }  
    return render(request,'checkout.html',context)
    


def _wishlist_id(request):

    wishlist = request.session.session_key
    if not wishlist:

        wishlist = request.session.create()
    return wishlist

def add_wishlist(request,product_id):
    current_user =request.user
    product = Product.objects.get(id=product_id)

    if current_user.is_authenticated:
        
        try:
            wishlist_item =WishlistItem.objects.get(product=product,user=current_user)
            # wishlistitem.quantity += 1
            wishlist_item.save()

        except WishlistItem.DoesNotExist:
            wishlist_item =WishlistItem.objects.create(
            product=product,
            # quantity =1,
            user =current_user,
        ) 
            wishlist_item.save()
    
        return redirect('wishlist') 
    #if user is not authenticated
    else:


        try:
            wishlist =Wishlist.objects.get(wishlist_id=_wishlist_id(request))

        except Wishlist.DoesNotExist:


            wishlist =Wishlist.objects.create(
            wishlist_id = _wishlist_id(request)
        )
        wishlist.save()


        try:
            wishlist_item =WishlistItem.objects.get(product=product,wishlist=wishlist)
            # cart_item.quantity += 1
            wishlist_item.save()

        except  WishlistItem.DoesNotExist:

            wishlist_item =WishlistItem.objects.create(
            product=product,
            # quantity =1,
            wishlist =wishlist,
        ) 
            wishlist_item.save()
    
        return redirect('wishlist')      
    



@login_required(login_url='login')
def wishlist(request,wishlist_items=None):

    try:
        # tax=0
        # grand_total=0
        if request.user.is_authenticated:
            wishlist_items = WishlistItem.objects.filter(user=request.user, is_active=True)


        else:
            wishlist = Wishlist.objects.get(wishlist_id = _wishlist_id(request))
            wishlist_items=WishlistItem.objects.filter(wishlist=wishlist,is_active=True)
        # for cart_item in cart_items:
            # total +=(cart_item.product.price * cart_item.quantity)
        #     quantity +=cart_item.quantity
        # tax = (3 * total)/100
        # grand_total = total + tax   
    except ObjectDoesNotExist:
        pass      



    context={
        # 'total':total,
        # 'quantity':quantity,
        'wishlist_items':wishlist_items,
        # 'tax'       :tax,
        # 'grand_total':grand_total,
    }  
    return render(request,'wishlist.html',context)



def remove_items_fully(request,product_id):
    current_user = request.user
    product = get_object_or_404(Product,id=product_id)

    if request.user.is_authenticated:

        wishlist_item =WishlistItem.objects.get(product=product,user=current_user)  

    else:
        wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))  
        wishlist_item= WishlistItem.objects.get(product=product,wishlist=wishlist)

    wishlist_item.delete()

    return redirect('wishlist')

# def test(request):
#     return render(request,'test.html')