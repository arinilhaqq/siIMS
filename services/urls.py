from django.urls import path
from .views import services_list, add_service, detail_view, delete_service, update_service

urlpatterns = [
    path('list-services/', services_list, name='services'),
    path('create-services/', add_service, name='add'),
    path('list-services/<int:id>', detail_view),
    path('list-services/<int:id>/delete', delete_service),
    path('list-services/<int:id>/update', update_service),
]