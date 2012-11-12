import re
from django import forms
from django.forms import ModelForm
from django.forms.widgets import RadioSelect
from django.contrib.auth.models import User
from models import Store

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name  = forms.CharField(max_length=20)
    email      = forms.EmailField()
    password   = forms.CharField(max_length=20, widget=forms.PasswordInput)
    mall_name  = forms.CharField(max_length=50)
    
    def create_user(self):
    	data = self.cleaned_data
    	email = data['email']
    	password = data['password']
    	first_name = data['first_name']
    	last_name = data['last_name']
    		
    	
    	username = re.sub('\.', '_', (re.sub('@', '_', email)))
    	user = User.objects.create_user(username, email, password)
    	user.first_name = first_name
    	user.last_name = last_name
    	
    	user.save()
    	return user
   
class AddStoreForm(forms.Form):
    name = forms.CharField(max_length=100)
    domain = forms.CharField(max_length=200)
    tags = forms.CharField(max_length=1000, required=False)
    #is_public = forms.
    
class EditFloorplanForm(forms.Form):
    store_id = forms.IntegerField()
    new_floor = forms.IntegerField()
    new_position = forms.IntegerField()

class WishlistItemForm(forms.Form):
    url = forms.CharField(max_length=2000)
    tags = forms.CharField(max_length=1000)
