from django.urls import path
from .import views

urlpatterns = [
    path('notajasa/', views.receipt_view),
    path('nota/notabarang/', views.barang_view),
    path('nota/', views.nota_list),
]