
from .models import Cart,CartItem
from .views import _cart_id
from .views import _wishlist_id
from .models import Wishlist,WishlistItem

def counter(request):
    cart_count = 0 
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=request.user)
            else:

                cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)                   


def counter_wishlist(request):
    wishlist_count = 0 
    if 'admin' in request.path:
        return {}
    else:
        try:
            wishlist = Wishlist.objects.filter(wishlist_id=_wishlist_id(request))
            if request.user.is_authenticated:
                wishlist_items = WishlistItem.objects.all().filter(user=request.user)
            else:

                wishlist_items = WishlistItem.objects.all().filter(wishlist=wishlist[:1])
            wishlist_count = 0
            for wishlist_item in wishlist_items:
                 
                wishlist_count += 1
        except Wishlist.DoesNotExist:
            wishlist_count = 0
    return dict(wishlist_count=wishlist_count)   