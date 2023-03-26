from django.urls import path
from . import views
from django.urls import path
from . import views

urlpatterns = [
    path('list-pelanggan/', views.pelanggan_list),
    path('create-pelanggan/', views.create_pelanggan),
    path('list-pelanggan/', views.detail_pelanggan),
    # path('detail-pelanggan/<int:id>', views.detail_pelanggan),
    path('delete-pelanggan/<int:id>', views.delete_pelanggan),
    path('update-pelanggan/<int:id>', views.update_pelanggan)
]