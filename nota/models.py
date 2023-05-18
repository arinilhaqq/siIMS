from django.db import models

class Nota(models.Model):
    nomor = models.IntegerField()
    tanggal = models.DateField()
    nomor_pkb = models.IntegerField()
    nomor_polisi = models.IntegerField()
    merk_type = models.CharField(max_length=70)
    pelanggan = models.CharField(max_length=70)
    appointment = models.OneToOneField('appointment.Appointment', on_delete=models.CASCADE)
    keterangan_lain_lain = models.CharField(max_length=70)
    total_harga_service = models.IntegerField()
    total_harga_sparepart = models.IntegerField()
    total_harga_lainlain = models.IntegerField(null=True)
    total_harga_gabungan = models.IntegerField()
    petugas_gudang = models.BooleanField(default=False)
    petugas_bengkel = models.BooleanField(default=False)
