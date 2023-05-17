from django.urls import path
from .import views

urlpatterns = [
    path('notajasa/', views.receipt_view),
    # path('create-final-inspection/<int:id>', views.create_final_inspection),
]