from  django import forms
from . models import Account
from django.forms import fields 



class RegistrationForm(forms.ModelForm):


    password=forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model=Account
        fields=['first_name','last_name','email','mobile','gender','password']

        

    def _init_(self,*args,**kwargs):
        super(RegistrationForm ,self)._init_(*args,**kwargs)  

        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
        


    def clean(self):

        cleaned_data    =super(RegistrationForm,self).clean()
        password        =cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')    

        if password != confirm_password:
            raise forms.ValidationError("Password does not match")



