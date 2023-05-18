from django.db import models
from pelanggan.models import Pelanggan
from karyawan.models import Karyawan
from services.models import Service

# class Appointment(models.Model):
#     pelanggan = models.ForeignKey(Pelanggan, on_delete=models.CASCADE)
#     teknisi = models.ForeignKey(Karyawan, on_delete=models.CASCADE, null=True, default=None)
#     date = models.DateField()
#     time = models.TimeField()
#     keluhan = models.TextField()
#     status = models.TextField(default='Not Ready')
#     services = models.ManyToManyField(Service, through='AppointmentService')
    
class Appointment(models.Model):
    pelanggan = models.ForeignKey(Pelanggan, on_delete=models.CASCADE)
    teknisi = models.ForeignKey(Karyawan, on_delete=models.CASCADE, null=True, default=None)
    date = models.DateField()
    time = models.TimeField()
    keluhan = models.TextField()
    status = models.TextField(default='Not Ready')
    services = models.ManyToManyField(Service, through='AppointmentService', related_name='appointments')

    def __str__(self):
        return f"Appointment {self.id} - {self.pelanggan.nama} - {self.date}"

# class AppointmentService(models.Model):
#     appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
#     services = models.ForeignKey(Service, on_delete=models.CASCADE)

class AppointmentService(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.appointment} - {self.service}"
