from django.urls import path
from . import views

urlpatterns = [
    path('create-karyawan/', views.create_karyawan),
    path('list-karyawan/', views.karyawan_list),
    path('detail-karyawan/<int:id>', views.detail_karyawan),
    path('delete-karyawan/<int:id>', views.delete_karyawan),
    path('update-karyawan/<int:id>', views.update_karyawan),
]