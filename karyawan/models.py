from django.db import models

KEHADIRAN_CHOICES = (
    ('Hadir', 'Hadir'),
    ('Tidak Hadir', 'Tidak Hadir'),
)

JABATAN_CHOICES = (
    ('owner', 'Owner'),
    ('akuntan', 'Akuntan'),
    ('inventori', 'Inventori'),
    ('service_advisor', 'Service Advisor'),
    ('teknisi', 'Teknisi'),
)

# Create your models here.
class Karyawan(models.Model):
    nama_karyawan = models.CharField(max_length=30)
    telepon_karyawan = models.BigIntegerField()
    alamat_karyawan = models.TextField()
    jabatan = models.CharField(max_length=15, choices=JABATAN_CHOICES, default='')
    kehadiran = models.CharField(max_length=15, choices=KEHADIRAN_CHOICES, default='0')
    total_keaktifan = models.IntegerField()
    email = models.EmailField()
    username = models.CharField(max_length=50, default='user')
    password = models.CharField(max_length=50, default='0000')
