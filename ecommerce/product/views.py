from django.shortcuts import render

from cart.models import CartItem
from .models import Product
from .models import *
from cart.views import _cart_id


def product_details(request,slug):
    item =Product.objects.get(slug=slug)
    # in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=item).exists()
    product_gallery = ProductGallery.objects.filter(product_id=item.id)  
    
    context = {
        'items': item,
        # 'in_cart':in_cart,
        'product_gallery':product_gallery,
    }
    return render(request,'product_details.html',context)
    


    
def about(request):
    return render(request,'about.html')



