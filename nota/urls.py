from django.urls import path
from .import views

urlpatterns = [
    path('nota/notajasa/<int:id>', views.receipt_view),
    path('nota/notabarang/<int:id>', views.barang_view),
    path('nota/notagabungan/<int:id>', views.gabungan_view),
    path('nota/', views.nota_list),
]