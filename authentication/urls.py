from django.urls import path
from .views import login, home, logout, forgot_password

# app_name = 'authentication'

urlpatterns = [
 path('', home, name='home'),
 path('login/', login, name='login'),
 path('logout/',logout,name ="logout"),
 path('forgot-password/',forgot_password,name ="forgot_password")
]