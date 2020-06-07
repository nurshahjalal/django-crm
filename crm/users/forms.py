from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
	
	email = forms.EmailField()
	first_name = forms.CharField(max_length=200)
	last_name = forms.CharField(max_length=200)
	phone = forms.CharField(max_length= 10)

	class Meta:

		model = User
		# These are the fields required to register user
		fields = ['username', 'first_name', 'last_name', 
			'email', 'phone', 'password1', 'password2']


class UserLoginForm(UserCreationForm):

	class Meta:

		model = User
		fields = ['username','password1']
		

class GetUsernameForm(UserCreationForm):
	email = forms.EmailField()
	class Meta:

		model = User
		fields = ['email']
