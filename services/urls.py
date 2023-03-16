from django.urls import path
from .views import services_list, add_service

urlpatterns = [
    path('list-services/', services_list, name='services'),
    path('create-services/', add_service, name='add'),
]
