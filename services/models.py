from django.db import models
# from multiselectfield import MultiSelectField
# from sparepart.models import SparePart

SATUAN_WAKTU = (('Menit', 'Menit'),
               ('Jam', 'Jam'),
               ('Hari', 'Hari'),
               ('Minggu', 'Minggu'),
               ('Bulan', 'Bulan'))

class Service(models.Model):

<<<<<<< HEAD
    nama = models.CharField(max_length=30, unique=True)
    harga = models.IntegerField()
    jumlah_estimasi_pengerjaan = models.IntegerField()
    satuan_waktu = models.CharField(max_length=30, choices=SATUAN_WAKTU, default='')
    kebutuhan_spare_parts = models.ManyToManyField('sparepart.SparePart', through='ServicePart')
=======
    nama = models.CharField(max_length=70, unique=True)
    harga = models.IntegerField()
    jumlah_estimasi_pengerjaan = models.IntegerField()
    satuan_waktu = models.CharField(max_length=30, choices=SATUAN_WAKTU, default='')
    kebutuhan_spare_part = models.ManyToManyField('sparepart.SparePart')
>>>>>>> a8a6b82b05b48c3ccf85412e2a6f702ae9c1ebd6

    def __str__(self):
        return self.nama

<<<<<<< HEAD
class ServicePart(models.Model):
    service = models.ForeignKey('services.Service', on_delete=models.CASCADE)
    part = models.ForeignKey('sparepart.SparePart', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
=======
# class ServicePart(models.Model):
#     service = models.ForeignKey('services.Service', on_delete=models.CASCADE)
#     part = models.ForeignKey('sparepart.SparePart', on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=0)
>>>>>>> a8a6b82b05b48c3ccf85412e2a6f702ae9c1ebd6
