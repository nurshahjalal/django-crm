from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from phone_field import PhoneField



class Customer(models.Model):

	# USer has one to one realtionship with Customer
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)                   
	# phone = models.CharField(max_length=10)
	phone = PhoneField(blank=True, help_text='Contact phone number')
	email = models.EmailField()
	image = models.ImageField(default='default.png', blank=True, null=True)
	date_created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f'{self.first_name}, {self.last_name}'
		



class Tag(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name


class Product(models.Model):

	CATEGORY = (
		('Indoor', 'Indoor'),
		('Outdoor', 'Outdoor')

		)
	
	name = models.CharField(max_length=200)
	price = models.DecimalField(max_digits=5, decimal_places=2)
	category = models.CharField(max_length=200, choices=CATEGORY)
	description = models.TextField()
	date_created = models.DateTimeField(default=timezone.now)
	tags = models.ManyToManyField(Tag)


	def __str__(self):
		return self.name




class Order(models .Model):

	STATUS = ( 
		('Pending', 'Pending'),
		('Out for delivery', 'Out for delivery'),
		('Delivered', 'Delivered')
		)

	# this 'customer' is referenced to Customer Table
	# on_delete=models.CASCADE >> if customer is deleted so as orders
	# on_delete=models.SET_NULL >> if customer is deleted orders will remain in db without customer info
	customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
	product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
	date_created = models.DateTimeField(default=timezone.now)
	choices = models.CharField(max_length=200, choices=STATUS)


	def __str__(self):
		return self.product.name
