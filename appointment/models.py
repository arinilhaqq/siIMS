from django.db import models
from pelanggan.models import Pelanggan
from karyawan.models import Karyawan
from services.models import Service


class Appointment(models.Model):
    pelanggan = models.ForeignKey(Pelanggan, on_delete=models.CASCADE)
    teknisi = models.ForeignKey(Karyawan, on_delete=models.CASCADE, null=True, default=None)
    date = models.DateField()
    time = models.TimeField()
    keluhan = models.TextField()
    status = models.TextField(default='Not Ready')
    # service = models.ForeignKey(Service, on_delete=models.CASCADE, default=None, null=True)
    services = models.ManyToManyField(Service)

