from django.urls import path
from . import views

urlpatterns = [
    path('create-services/', views.create_services)
]