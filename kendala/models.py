from django.db import models
from appointment.models import Appointment, AppointmentService
from services.models import Service

# Create your models here.

SATUAN_WAKTU = (('Menit', 'Menit'),
               ('Jam', 'Jam'),
               ('Hari', 'Hari'),
               ('Minggu', 'Minggu'),
               ('Bulan', 'Bulan'))

STATUS = (('Unsolved', 'Unsolved'),
          ('Solved', 'Solved'))

# class Kendala(models.Model):
#     appointment_service = models.ForeignKey(AppointmentService, on_delete=models.CASCADE)
#     deskripsi = models.TextField(blank=True, null=True)
#     status = models.BooleanField(default=False)
#     jumlah_estimasi_pengerjaan = models.IntegerField()
#     satuan_waktu = models.CharField(max_length=30, choices=SATUAN_WAKTU, default='')

# class Kendala(models.Model):
#     appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True)
#     deskripsi = models.TextField(blank=True, null=True)
#     status = models.BooleanField(default=False)
#     jumlah_estimasi_pengerjaan = models.IntegerField()
#     satuan_waktu = models.CharField(max_length=30, choices=SATUAN_WAKTU, default='')

class Kendala(models.Model):
    appointment_service = models.ForeignKey(AppointmentService, on_delete=models.CASCADE, null=True)
    deskripsi = models.TextField(blank=True, null=True)
    status = models.CharField(default='Unsolved', choices=STATUS, max_length=30)
    jumlah_estimasi_pengerjaan = models.IntegerField()
    satuan_waktu = models.CharField(max_length=30, choices=SATUAN_WAKTU, default='')
