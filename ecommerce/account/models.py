from django.db import models
from ast import Return
import uuid
from django.contrib.auth.models import  BaseUserManager, AbstractBaseUser

from django.db.models.fields import UUIDField


# Create your models here.

class AccountManager(BaseUserManager):
    def create_user(self,first_name,last_name,email,mobile,gender,password=None,is_staff=False):
        
        if not email:
            raise ValueError('must have an email')

        if not mobile:
            raise ValueError('must have an number')    

        user=self.model(
            email  = self.normalize_email(email),
            mobile = mobile,
            first_name = first_name,
            last_name = last_name,
            gender = gender,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,first_name,last_name,gender,mobile,password):
    
        user = self.create_user(
            email = self.normalize_email(email),
            mobile =mobile,
            first_name= first_name,
            last_name= last_name,
            password=password,
            gender=gender,
        )
        user.is_admin   = True
        user.is_active  = True
        user.is_staff  = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

GENDER = (
    ('Male', 'Male'),('Female','Female'),
)        


class Account(AbstractBaseUser):
    first_name   = models.CharField(max_length=100)
    last_name     = models.CharField(max_length=100)  
    email         = models.EmailField(max_length=100,unique=True)
    mobile        = models.CharField(max_length=10,unique=True,null=True)
    gender        = models.CharField(max_length=10,choices=GENDER,null=True,blank=False)
    is_staff      = models.BooleanField(default=False)
    is_active     = models.BooleanField(default=True)
    is_admin      = models.BooleanField(default=False)
    is_verified   = models.BooleanField(default=False)
    otp_verified  = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','mobile','gender']

    objects=AccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True

class Address(models.Model):
    id               =  models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user             =  models.ForeignKey(Account,on_delete=models.CASCADE)
    full_name        =  models.CharField(max_length=100)
    address_line_1   =  models.CharField(max_length=100)
    city             =  models.CharField(max_length=100)
    pin_code         =  models.BigIntegerField()
    state            =  models.CharField(max_length=50,null=True)
    country          =  models.CharField(max_length=50)
    mobile           =  models.BigIntegerField()
    landmark         =  models.CharField(max_length=50)
    default          =  models.BooleanField(default=False)

    class Meta:
        verbose_name        =   "Address"
        verbose_name_plural =   "Addresses"
