from django.urls import path
from . import views

urlpatterns = [
	path('', views.dashboard, name='account-dashboard'),
	path('products/', views.products, name='account-products'),
	path('customer/', views.customer, name='account-customer'),
	path('customer/<int:pk>/', views.customer_detail, name='account-cust_detail'),
	path('orders/', views.orders_view, name='account-orers'),
	path('user/', views.user_page, name='user-page'),
	path('settings/', views.user_settings, name='user-settings'),
	path('create_order/', views.create_order, name='order-create'),
	path('create_order/<int:pk>', views.create_customer_order, name='create-customer-order'),
	path('update_order/<int:pk>/', views.update_order, name='order-update'),
	path('delete_order/<int:pk>/', views.delete_order, name='order-delete'),

]