from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
path('register/', views.register, name='register'),
path('login/', views.user_login, name='user-login'),
path('logout/', views.user_logout, name='user-logout'),

path('username/', views.retrieve_username, name='retrieve-username'),

path('reset_password', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), 
	name='password_reset' ),
path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), 
	name='password_reset_done'),
path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), 
	name='password_reset_confirm'),
path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), 
	name='password_reset_complete'),
]