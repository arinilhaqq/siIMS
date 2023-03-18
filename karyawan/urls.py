from django.urls import path
from . import views

urlpatterns = [
    path('create-karyawan/', views.create_karyawan),
    path('list-karyawan/', views.karyawan_list),
]