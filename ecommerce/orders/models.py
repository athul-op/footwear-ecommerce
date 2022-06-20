from django.db import models
from account.models import Account
from product.models import Product





class Payment(models.Model):
    
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True) 
    name =models.CharField(max_length=100,null=True )
    amount = models.CharField(max_length=100)
    order_id =models.CharField(max_length=100,blank=True)
    razorpay_payment_id= models.CharField(max_length=100, blank=True,null=True)  
    payment_method=models.CharField(max_length=100)
    paid =models.BooleanField(default=False)
    created_at=models.DateField(auto_now_add=True)

    


class Order(models.Model):
    STATUS =(
        ('New','New'),
        ('Accepted','Accepted'),
        ('Completed','Completed'),
        ('Cancelled','cancelled'),
    )

    user =models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)
    Payment=models.ForeignKey(Payment,on_delete=models.SET_NULL,null=True)
    order_number = models.CharField(max_length=100)
    first_name =models.CharField(max_length=50)
    last_name= models.CharField(max_length=50)
    phone=models.CharField(max_length=15)
    email=models.EmailField(max_length=50)
    address_line_1=models.CharField(max_length=50)
    address_line_2=models.CharField(max_length=50,blank=True)
    country=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    order_note=models.CharField(max_length=100,blank=True)
    order_total=models.FloatField()
    tax=models.FloatField()
    status=models.CharField(max_length=10,choices=STATUS,default='New')
    ip = models.CharField(blank=True,max_length=20)
    is_ordered =models.BooleanField(default=False)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)
    payment_method   = models.CharField(max_length=100,null=True,blank=True)


    def full_name(self):
        return f'{self.first_name} {self.last_name}' 


    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'

    def _str_(self):
        return self.first_name 



class OrderProduct(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    payment=models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    user =models.ForeignKey(Account,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    product_price=models.FloatField()
    ordered=models.BooleanField(default=False)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)


    def _str_(self):
        return self.product.product_name        
        
