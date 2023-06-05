from django.urls import path
from .views import services_list, add_service, delete_service, update_service, add_kebutuhan_spare_parts
urlpatterns = [
    path('list-services/', services_list),
    path('create-services/', add_service),
    path('delete-services/<int:id>', delete_service),
    path('update-services/<int:id>', update_service),
    path('add-spareparts/<int:id>', add_kebutuhan_spare_parts),
]