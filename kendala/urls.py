from django.urls import path
from . import views

urlpatterns = [
    path('create-kendala/<int:id>', views.create_kendala),
    # path('list-karyawan/', views.karyawan_list),
    # path('detail-karyawan/<int:id>', views.detail_karyawan),
    # path('delete-karyawan/<int:id>', views.delete_karyawan),
    # path('update-karyawan/<int:id>', views.update_karyawan),
]