from django.urls import path
from . import views
from .models import InitialInspection

urlpatterns = [
    path('create-initial-inspection/<int:id>', views.create_initial_inspection),
    path('detail-initial-inspection/<int:id>', views.detail_initial_inspection),
]