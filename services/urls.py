from django.urls import path
from .views import detail_service, services_list, add_service, delete_service, update_service

urlpatterns = [
    path('list-services/', services_list),
    path('create-services/', add_service),
    path('delete-services/<int:id>', delete_service),
    path('update-services/<int:id>', update_service),
    path('list-services/', detail_service),
]