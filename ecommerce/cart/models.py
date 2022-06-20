from tkinter import CASCADE
from django.db import models

from product.models  import Product
from account.models import *



class Cart(models.Model):

    cart_id    = models.CharField(max_length=250,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)




    def str(self):

        return self.cart_id




class CartItem(models.Model):
    user    =models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True ,null=True)
    cart    = models.ForeignKey(Cart,on_delete=models.CASCADE,blank=True ,null=True) 
    quantity =models.IntegerField()   
    is_active = models.BooleanField(default=True)  


    def sub_total(self):

        return self.product.price * self.quantity

    

    
    def str(self):

        return self.product



class Wishlist(models.Model):

    wishlist_id    = models.CharField(max_length=250,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)




    def str(self):

        return self.wishlist_id







class  WishlistItem(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    wishlist    = models.ForeignKey(Wishlist,on_delete=models.CASCADE,null=True)   
    is_active = models.BooleanField(default=True) 


    def __unicode__(self):
        return self.product