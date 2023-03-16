from django.db import models


class Service(models.Model):
    nama = models.CharField(max_length=30)
    harga = models.CharField(max_length=10)
    estimasi_pengerjaan = models.CharField(max_length=10)

