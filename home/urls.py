from django.urls import path
from . import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage),
    path('change-password/', views.change_password),
    path('update-password/<str:username>', views.update_password),
    path('dashboard/', views.dashboard),
    path('dashboard-appointment-date/', views.appointment_chart_date, name='appointment_chart_date'),
    path('dashboard-appointment-week/', views.appointment_chart_week, name='appointment_chart_week'),
    path('dashboard-appointment-month/', views.appointment_chart_month, name='appointment_chart_month'),
    path('dashboard-appointment-customer/', views.appointment_chart_top_customers, name='appointment_chart_top_customers'),
    path('dashboard-sparepart-stok/', views.sparepart_chart_stock, name='sparepart_chart_stock'),
    path('dashboard-appoinment-karyawan/', views.appointment_chart_top_karyawan, name='appointment_chart_top_karyawan'),
]