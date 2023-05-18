from django.urls import path
from .import views

urlpatterns = [
    path('nota/notajasa/', views.receipt_view),
    path('nota/notabarang/', views.barang_view),
    path('nota/notagabungan/', views.gabungan_view),
    path('nota/', views.nota_list),
]