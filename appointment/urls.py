from django.urls import path
from . import views
from .models import Pelanggan

urlpatterns = [
    path('create-appointment/', views.create_appointment),
    path('list-appointment/', views.list_appointment),
    path('finished-appointment/<int:id>', views.teknisi_finished_appointment),
    path('delete-appointment/<int:id>', views.delete_appointment),
    path('possible-service/<int:id>', views.possible_service),
    path('service-appointment/<int:id>', views.list_service_appointment),
    path('estimasi-appointment/<int:id>', views.estimasi_appointment),
]