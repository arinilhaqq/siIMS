from django.db import models

# from services.models import Service
# Create your models here.

class SparePart(models.Model):
    nama = models.CharField(max_length=30)
    variasi = models.CharField(max_length=30)
    harga = models.IntegerField(default='')
    stok = models.IntegerField(default='')
    services = models.ManyToManyField('services.Service')

    def __str__(self):
        return f"{self.nama} {self.variasi}"