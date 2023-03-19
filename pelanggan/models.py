from django.db import models

# Create your models here.
class Pelanggan(models.Model):
    nama_pelanggan = models.CharField(max_length=30)
    telepon_pelanggan = models.CharField(max_length=15)
    alamat_pelanggan = models.TextField()
    jenis_mobil = models.CharField(max_length=30)
    nama_mobil = models.CharField(max_length=30)
    nomor_pkb =models.IntegerField()
    nomor_polisi = models.CharField(max_length=10)
    email = models.EmailField()

