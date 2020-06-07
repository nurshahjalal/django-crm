from django.http import HttpResponse
from django.shortcuts import redirect



"""
these are the custom decorator

"""
# wherever this decorator is called it takes the 
# method as a parameter

# purpose :
# check if the user is logged in ,
# redicrect the user to home page if  user wants to login or register
def authentications(view_func):

	def wrapper_func(request, *args, **kwargs):

		if request.user.is_authenticated:
			return redirect('account-dashboard')
		else:
			return view_func(request, *args, **kwargs)
	return wrapper_func



# this is the way we can pass argument in decorator
def allowed_users(allowed_roles=[]):

	def decorator(func):
		def wrapper_func(request, *args, **kwargs):

			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name

			if group in allowed_roles:
				return func(request, *args, **kwargs)
			else:
				return HttpResponse('You Are Not Authorized.')				
		return wrapper_func
	return decorator


def admin_only(func):
	def wrapper_func(request, *args, **kwargs):

		group = None

		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group == 'customer':
			return redirect('user-page')

		if group == 'admin':
			return func(request, *args, **kwargs)

		
	return wrapper_func


	



