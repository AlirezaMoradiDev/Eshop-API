from django.urls import path
from . import views
from rest_framework.authtoken import views as token_views


app_name = 'user'
urlpatterns = [
    path('check', views.check_token, name='check'),
    path('login', token_views.obtain_auth_token, name='login'),
    path('reg', views.register, name='register')
]
