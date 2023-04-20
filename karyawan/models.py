from django.db import models

KEHADIRAN_CHOICES = (
    ('Hadir', 'Hadir'),
    ('Tidak Hadir', 'Tidak Hadir'),
)

JABATAN_CHOICES = (
    ('Admin', 'Admin'),
    ('Owner', 'Owner'),
    ('Akuntan', 'Akuntan'),
    ('Inventori', 'Inventori'),
    ('Service Advisor', 'Service Advisor'),
    ('Teknisi', 'Teknisi'),
)

class Karyawan(models.Model):
    nama_karyawan = models.CharField(max_length=30)
    telepon_karyawan = models.CharField(max_length=15)
    alamat_karyawan = models.TextField()
    jabatan = models.CharField(max_length=15, choices=JABATAN_CHOICES, default='')
    kehadiran = models.CharField(max_length=15, choices=KEHADIRAN_CHOICES, default='0')
    total_keaktifan = models.IntegerField(default='0')
    email = models.EmailField()
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50, default='0000')