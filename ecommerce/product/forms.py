from  django import forms
from django.forms import fields    
# from . models import Account
from .models import *


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','category','description','price','stock','image','slug']

    def __init__(self,*args,**kwargs):
        super(ProductForm,self).__init__(*args,**kwargs)    

        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'