from django.db import models

class NotaBarang(models.Model):
    nomor_barang = models.IntegerField()
    total_harga_sparepart = models.IntegerField()
    petugas_gudang = models.BooleanField(default=False)
    petugas_bengkel = models.BooleanField(default=False)

class NotaJasa(models.Model):
    nomor_jasa = models.IntegerField()
    total_harga_service = models.IntegerField()

class NotaGabungan(models.Model):
    nomor_gabungan = models.IntegerField()
    tanggal = models.DateField()
    appointment = models.OneToOneField('appointment.Appointment', on_delete=models.CASCADE)
    keterangan_lain_lain = models.CharField(max_length=70, null=True)
    nota_barang = models.ForeignKey(NotaBarang, on_delete=models.CASCADE)
    nota_jasa = models.ForeignKey(NotaJasa, on_delete=models.CASCADE)
    total_harga_service = models.IntegerField()
    total_harga_sparepart = models.IntegerField()
    total_harga_lainlain = models.IntegerField(null=True)
    total_harga_gabungan = models.IntegerField()