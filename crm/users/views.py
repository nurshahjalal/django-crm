from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .forms import UserRegisterForm, UserLoginForm, GetUsernameForm
from account.decorators import authentications
from account.models import Customer
from crm.settings import EMAIL_HOST_USER


def register(request):

	form = UserRegisterForm()
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			current_user = form.save()
			print(f'current_user : {current_user}')
			# get the username from form
			user = form.cleaned_data.get('username')
			first_name = form.cleaned_data.get('first_name')
			last_name = form.cleaned_data.get('last_name')
			phone = form.cleaned_data.get('phone')
			print(phone)
			email = form.cleaned_data.get('email')

			
			# get customer group
			group = Group.objects.get(name='customer')
			
			# add the current user to customer group
			current_user.groups.add(group)

			# the same way we can make user as customer
			# since Customer has one to one relation with User
			# and it has user attribute 
			Customer.objects.create(user=current_user, first_name=first_name, last_name=last_name,
				phone=phone, email=email)

			messages.success(request, f'You account is created successfully! {user}')
			return redirect('user-login')
	else:

		form = UserRegisterForm()

	context = {'form': form}
	return render (request, 'users/register.html', context)

@authentications
def user_login(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		
		if user is not None:
			login(request, user)
			return redirect('account-dashboard') # whatever the page 
		else:
			messages.info(request, "Username or password is incorrect")
	
	context = {}	
	return render(request, 'users/login.html', context)



def user_logout(request):
	logout(request)
	messages.info(request, "You have successfully looged out")
	return redirect('user-login')


def retrieve_username(request):

	form = GetUsernameForm()

	if request.method == 'POST':

		email = request.POST.get('email')

		user_name = User.objects.filter(email=email).first()
		if user_name is not None:
			user = user_name.username


			subject = 'Requested Username'
			from_email = EMAIL_HOST_USER
			context = {'user': user}
			html_content = render_to_string('users/email_template.html', 
				{'title':'Test Email', 'user':user})
			text_content = strip_tags(html_content)

			email = EmailMultiAlternatives( 
				subject, 
				text_content, 
				from_email,
				[email]
				)

			email.attach_alternative(html_content, 'text/html')
			email.send()


			# text_content = 'This is an automated email from django team'
			# html_content = '<p> Your Requested Username Is :<br> <strong> ' + user + '</strong>'
			# msg = EmailMessage(subject, html_content, from_email, [email])
			# msg.content_subtype = "html"  # Main content is now text/html
			# msg.send()




			# msg = EmailMultiAlternatives(subject, text_content, from_, [to_])
			# msg.attach_alternative(html_content, 'text/html')
			# msg.send()

			#send_mail(subject, body, from_, to_, fail_silently=False)
			return redirect('password_reset_done')
   
		else:
			print("No Username is Found with this: " + email)

	context = {}	
	return render(request, 'users/username.html', context)
