from django.urls import path
from . import views
from .models import Pelanggan

urlpatterns = [
    path('create-appointment/', views.create_appointment),
    path('list-appointment/', views.list_appointment),
    path('finished-appointment/<int:id>', views.teknisi_finished_appointment),
]