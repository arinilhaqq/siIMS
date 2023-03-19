from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage),
    path('change-password/', views.change_password),
]