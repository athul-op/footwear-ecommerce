from django.shortcuts import render,redirect
from cart.models import CartItem
from .forms import OrderForm
from .models import Order,OrderProduct
from datetime import date
from .models import Payment
from .forms import PaymentForm
from django.views.decorators.csrf import csrf_exempt
import razorpay
from product.models import Product
from django.conf import settings
from coupons.models import Coupon,CouponUsers


# def payments(request):
#     return render(request,'payments.html')

def place_order(request, total=0,coupon=0,quantity=0,):
    current_user = request.user
# cart count lessthan or equal to zero redirect shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <=0:
        return redirect('home')
    
    if CouponUsers.objects.filter(user=request.user, is_used= False).exists():
        coupon_user = CouponUsers.objects.get(user=request.user, is_used= False)
        coupon      = coupon_user.amount
    grand_total =0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity 
    tax = (3 * total)/100
    grand_total = total + tax - coupon



    if request.method == 'POST':
        form =OrderForm(request.POST)
        
        if form.is_valid():
        
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax 
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # generate ordernumber
            yr = int(date.today().strftime('%Y'))
            dt = int(date.today().strftime('%d'))
            mt = int(date.today().strftime('%m'))
            d = date(yr,mt,dt)
            current_date = d.strftime('%Y%m%d')
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user,is_ordered=False, order_number = order_number)
            print(order)
            request.session['order_number']= order_number
            context={
                'order' : order,
                'cart_items' : cart_items,
                'total' : total,
                'tax' : tax,
                'grand_total' : grand_total,
            }
            return render(request,'payments.html',context)       
    
    return redirect('checkout')






@csrf_exempt
def payments(request):
    user = request.user
    order_id=request.session['order_number']
    order=Order.objects.get(order_number=order_id)   
    cart_items =CartItem.objects.filter(user=user)
    grand_total =0
    tax = 0
    total= 0
    quantity=0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity 
    tax = (3 * total)/100
    grand_total = total + tax 
    # total=request.session['total']
    # tax=request.session['tax']
    # grand_total=request.session['grand_total']

    if request.method =='POST':
        
        name = user.first_name
        amount =grand_total * 100


        # create razorpay client
    
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
        # create order
        response_payment = client.order.create(dict(amount=amount,
                                                    currency='INR')
                                                ) 
        
        order_id =response_payment['id']
        order_status= response_payment['status'] 

        if order_status == 'created':
            payment =Payment(
                name = name,
                amount = amount,
                order_id = order_id,
                
            )
            payment.save()       
            response_payment['name']=name

            form = PaymentForm(request.POST or None)

            context={
                'form':form,
                'payment':response_payment,
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'tax':tax,
                'grand_total':grand_total,
            }
            return render(request,'payments.html',context)

    form = PaymentForm()
    return render(request,'payments.html',{'form':form ,'order':order})

@csrf_exempt
def payment_status(request,order_number):
    response = request.POST
    params_dict ={
        'razorpay_order_id':response['razorpay_order_id'],
        'razorpay_payment_id':response['razorpay_payment_id'],
        'razorpay_signature':response['razorpay_signature']
    }

    #client instance

    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
    try:
        status = client.utility.verify_payment_signature(params_dict)
        payment =Payment.objects.get(order_id=response['razorpay_order_id']) 
        payment.razorpay_payment_id=response['razorpay_payment_id']
        payment.payment_method='Razorpay'
        payment.paid = True 

        
        payment.save()


        order_number=request.session['order_number'] 
        print(order_number)
        order= Order.objects.get(order_number=order_number) 
        order.payment= payment
        order.is_ordered = True
        order.payment_method = 'razorpay'
        order.save()

        # move the cart item to orderproduct table
        cart_items=CartItem.objects.filter(user=request.user)

        for item in cart_items:
            orderProduct = OrderProduct()
            orderProduct.order_id = order.id
            orderProduct.payment = payment
            orderProduct.user_id = request.user.id
            orderProduct.product_id = item.product_id
            orderProduct.quantity = item.quantity
            orderProduct.product_price = item.product.price
            orderProduct.ordered = True
            orderProduct.save()

            product=Product.objects.get(id=item.product_id)
            product.stock -=item.quantity
            product.save()

        #clear cart
        CartItem.objects.filter(user=request.user).delete()
        if CouponUsers.objects.filter(user=request.user, is_used= False).exists():

           coupon_user = CouponUsers.objects.get(user=request.user, is_used= False)
           coupon_user.is_used = True
           coupon_user.save() 
        
        return render(request,'order_complete.html',{'status':True}) 


    except:
        return render(request,'order_complete.html',{'status':False})



def cash_on_delivery(request) :
    if request.method == 'POST' :
        try :
            order_number = request.session['order_number']
            order= Order.objects.get(order_number= order_number) 
            order.is_ordered = True
            order.payment_method = 'cash on delivery'
            
            order.save()
            
            # move the cart item to orderproduct table
            cart_items=CartItem.objects.filter(user=request.user)
            print(cart_items)

            for item in cart_items:
                order_product = OrderProduct.objects.create(
                order_id = order.id,
                user_id = request.user.id,
                product_id = item.product_id,
                quantity = item.quantity,
                product_price = item.product.price,
                ordered = True,
                )
                order_product.save()
                #reduce the quantity of sold products 
                product=Product.objects.get(id=item.product_id)
                product.stock -=item.quantity
                product.save()

                #clear cart
            CartItem.objects.filter(user=request.user).delete()      
            if CouponUsers.objects.filter(user=request.user, is_used= False).exists():

               coupon_user = CouponUsers.objects.get(user=request.user, is_used= False)
               coupon_user.is_used = True
               coupon_user.save()   
            return render(request,'order_complete.html',{'status':True})
        except :
            # return redirect('cart')         
            return render(request,'order_complete.html',{'status':False})