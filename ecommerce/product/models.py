from django.db import models
from category.models import Category
# from account.models import Account
# from django.urls import reverse
# # Create your models here.



class Product(models.Model):
    name         = models.CharField(max_length=100 , null=True)
    category     = models.ForeignKey(Category,on_delete=models.CASCADE)
    slug         = models.SlugField(max_length=200, db_index=True,null=True)
    price        = models.FloatField()
    image        = models.ImageField (upload_to="images/product")
    description  = models.TextField(max_length=1000)
    available    = models.BooleanField(default=True, verbose_name="available")
    stock        = models.PositiveIntegerField(default=0)


 
    def __str__(self):
        return self.name

class ProductGallery(models.Model):
    product = models.ForeignKey(Product,default=None,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/product")

    def __str__(self):
        return self.product.name






# class Review(models.Model):
#     product     =   models.ForeignKey(Product,on_delete=models.CASCADE)
#     user        =   models.ForeignKey(Account,on_delete=models.CASCADE)
#     subject     =   models.CharField(max_length=200 , blank=True)
#     review      =   models.TextField(null=True,blank=True)
#     rating      =   models.IntegerField()
#     created_at  =   models.DateTimeField(auto_now_add=True)




