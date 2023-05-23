from django.urls import path
from .views import sparepart_list, add_sparepart, delete_sparepart, update_sparepart, ambil_service

urlpatterns = [
    path('list-sparepart/', sparepart_list),
    path('create-sparepart/', add_sparepart),
    path('delete-sparepart/<int:id>', delete_sparepart),
    path('update-sparepart/<int:id>', update_sparepart),
]