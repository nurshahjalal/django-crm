import django_filters
from django_filters import DateFilter
from .models import *


class OrderFilter(django_filters.FilterSet):

	# custom filter
	# field_name = field from model which is mapped
	# lookup_expr = look up expression 
	# gte = greater than or equal to
	start_date = DateFilter(field_name='date_created', lookup_expr='gte')
	# lte = less than or equal to
	end_date = DateFilter(field_name='date_created', lookup_expr='lte')

	# charFiter is the partial or full text search
	# icontains = case insensative
	# note =  CharFilter(field_name='note', lookup_expr='icontains')

	class Meta:
		model = Order
		fields = '__all__'

		exclude = ['customer', 'date_created']