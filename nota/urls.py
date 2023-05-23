from django.urls import path
from .import views
# from .views import print_pdf

urlpatterns = [
    path('nota/notajasa/<int:id>', views.receipt_view),
    path('nota/notabarang/<int:id>', views.barang_view),
    path('nota/notagabungan/<int:id>', views.gabungan_view),
    path('nota/notagabungan/update-notagabungan/<int:id>', views.update_notagabungan),
    path('nota/notabarang/ceklis-notabarang/<int:id>', views.ceklis_notabarang),
    path('nota/', views.nota_list),
    # path('print-pdf/<int:id>/', print_pdf, name='print_pdf'),
]