from django.urls import path
from .views import detail_sparepart, sparepart_list, add_sparepart, delete_sparepart, update_sparepart

urlpatterns = [
    path('list-sparepart/', sparepart_list),
    path('create-sparepart/', add_sparepart),
    path('delete_sparepart/<int:id>', delete_sparepart),
    path('update-sparepart/<int:id>', update_sparepart),
    path('list-sparepart/', detail_sparepart),
]