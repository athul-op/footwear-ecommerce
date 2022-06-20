from cart import views
from django.urls import path

from cart.views import add_wishlist

urlpatterns =[
    path('',views.cart,name='cart'),
    path('add_cart/<int:product_id>/',views.add_cart,name='add_cart'),
    path('remove_cart/<int:product_id>/',views.remove_cart,name="remove_cart"),
    path('remove_item_fully/<int:product_id>/',views.remove_item_fully,name='remove_item_fully'),
    # path('test',views.test,name='test'),
    path('checkout/',views.checkout, name='checkout'),
    
    path('wish',views.wishlist,name='wishlist'),
    path('add_wishlist/<int:product_id>/',views.add_wishlist,name='add_wishlist'),
    # # path('remove_wishlist/<int:product_id>/',views.remove_wishlist,name="remove_wishlist"),
    path('remove_items_fully/<int:product_id>/',views.remove_items_fully,name='remove_items_fully'),
    path('add_coupon',views.add_coupon,name='add_coupon'),
]