from django.urls import path
from . import views
from .models import FinalInspection

urlpatterns = [
    path('create-final-inspection/<int:id>', views.create_final_inspection),
    path('update-final-inspection/<int:id>', views.update_final_inspection),
    path('verify-final-inspection/<int:id>', views.verify_final_inspection),
]