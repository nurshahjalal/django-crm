from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from .models import Customer, Tag, Product, Order
from .forms import OrderForm, CustomerForm
from .filters import OrderFilter
from .decorators import authentications, allowed_users, admin_only

# class AccountListView(generic.ListView):	
# 	model = Account

@login_required(login_url='user-login')
@admin_only
def dashboard(request):
	# this is home page
	customers = Customer.objects.all().order_by('-last_name')
	total_customer = customers.count()
	orders = Order.objects.all()
	print(orders)

	limit_order = orders.order_by('-date_created')[:5]

	# orders = order_by('-date_created')
	total_order = orders.count()
	print(f'total_order : {total_order}')

	total_delivered_count = orders.filter(choices='Delivered').count()
	total_out_for_delivery_count = orders.filter(choices='Out for delivery').count()
	total_pending_count = orders.filter(choices='Pending').count()

	context = {'customers':customers, 'orders':orders, 
	'total_order': total_order, 'limit_order': limit_order,
	'total_delivered_count': total_delivered_count, 
	'total_out_for_delivery_count': total_out_for_delivery_count, 
	'total_pending_count': total_pending_count
	}
	return render(request, 'account/dashboard_list.html', context)



@login_required(login_url='user-login')
@allowed_users(allowed_roles=['admin'])
def products(request):
	prod = Product.objects.all()
	return render(request, 'account/products_list.html', {'prod':prod})



@login_required(login_url='user-login')
@allowed_users(allowed_roles=['admin'])
def customer(request):
	# orders = Order.objects.all()
	# ordFilter = OrderFilter(request.GET, queryset=orders)
	# orders = ordFilter.qs
	# context = {'orders': orders, 'ordFilter': ordFilter}
	cust = Customer.objects.all()
	context = {'cust':cust}
	return render(request, 'account/customer_list.html', context)



@login_required(login_url='user-login')
@allowed_users(allowed_roles=['customer'])
def user_page(request):
	#finding the particular customer orders
	# user and customer has one to one relationship in Customer model
	# we can tell, logged in user is the customer
	orders = request.user.customer.order_set.all()

	total_order = orders.count()

	total_delivered_count = orders.filter(choices='Delivered').count()
	total_out_for_delivery_count = orders.filter(choices='Out for delivery').count()
	total_pending_count = orders.filter(choices='Pending').count()

	context = {'orders':orders, 
	'total_order': total_order,
	'total_delivered_count': total_delivered_count, 
	'total_out_for_delivery_count': total_out_for_delivery_count, 
	'total_pending_count': total_pending_count
	}

	return render(request, 'account/user.html', context)




@login_required(login_url='user-login')
@allowed_users(allowed_roles=['admin', 'customer'])
def customer_detail(request, pk):
	customer = Customer.objects.get(id=pk)
	orders = customer.order_set.all()
	context = {'customer': customer, 'orders': orders}
	return render(request, 'account/customer_detail.html', context)


@login_required(login_url='user-login')
@allowed_users(allowed_roles=['admin'])
def orders_view(request):
	#showing latest orders first
	orders = Order.objects.all().order_by('-date_created')
	context = {'orders': orders}
	return render(request, 'account/orders_list.html', context)


@login_required
@allowed_users(allowed_roles=['admin'])
def create_order(request):
	form = OrderForm()
	
	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, f'Your order has been created successfully')
			return redirect('account-dashboard')

	context = {'form': form}
	return render(request, 'account/orders_form.html', context)


@login_required(login_url='user-login')
@allowed_users(allowed_roles=['admin'])
def create_customer_order(request, pk):

	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'choices'), extra=5)
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
	# form = OrderForm(initial={'customer': customer})
	if request.method == 'POST':
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			messages.success(request, f'Your order has been created successfully')
			return redirect('/')

	context = {'formset': formset}
	return render(request, 'account/customer_order_form.html', context)


@login_required(login_url='user-login')
@allowed_users(allowed_roles=['admin'])
def update_order(request, pk):
	
	# getting the order id that needs to be updated
	order = Order.objects.get(id=pk)
	# 'instance' means it will prefilled with certain order (the order with id=pk) , in this case 
	# above 'order' has been passed to the form to be preloaded
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		form.save()
		return redirect('/')

	context = {'form': form}
	return render(request, 'account/orders_form.html', context)


@login_required(login_url='user-login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, pk):

	order = Order.objects.get(id=pk)

	if request.method == 'POST':
		order.delete()
		return redirect('/')
	context = {'item': order}
	return render(request, 'account/delete_order.html', context)


@login_required(login_url='user-login')
@allowed_users(allowed_roles=['customer'])
def user_settings(request):

	cust = request.user.customer
	form = CustomerForm(instance=cust)
	
	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES, instance=cust)
		form.save()
		messages.success(request, f'Your profile has been updated successfully')

	context = {'form': form}

	return render(request, 'account/account_settings.html', context)
