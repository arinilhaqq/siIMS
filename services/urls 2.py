from django.urls import path
from .views import services_list, add_service

urlpatterns = [
    path('', services_list, name='services'),
    path('addservice/', add_service, name='add'),
]
