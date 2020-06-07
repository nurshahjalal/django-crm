from django.db import models
from django.contrib.auth.models import User

"""

this is the model for User's Profile, using django's existing User class.
with One To One relation between user and Profile, each user will have one profile
and each profile will have one user

"""

class Profile(models.Model):

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	Address1 = models.CharField(max_length=200, null=True, blank=True)
	Address2 = models.CharField(max_length=200, null=True, blank=True)
	City = models.CharField(max_length=200, null=True, blank=True)
	Zip = models.CharField(max_length=200, null=True, blank=True)
	State = models.CharField(max_length=200, null=True, blank=True)
	Country = models.CharField(max_length=200, null=True, blank=True)
	image = models.ImageField(default='default.jpg', upload_to='Profile_Pic')

	def __str__(self):
		return f'{self.user.username} Profile'