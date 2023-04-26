from django.db import models
# from multiselectfield import MultiSelectField
# from sparepart.models import SparePart

SATUAN_WAKTU = (('Menit', 'Menit'),
               ('Jam', 'Jam'),
               ('Hari', 'Hari'),
               ('Minggu', 'Minggu'),
               ('Bulan', 'Bulan'))

class Service(models.Model):

    nama = models.CharField(max_length=70, unique=True)
    harga = models.IntegerField()
    jumlah_estimasi_pengerjaan = models.IntegerField()
    satuan_waktu = models.CharField(max_length=30, choices=SATUAN_WAKTU, default='')
    kebutuhan_spare_part = models.ManyToManyField('sparepart.SparePart')

    def __str__(self):
        return self.nama

# class ServicePart(models.Model):
#     service = models.ForeignKey('services.Service', on_delete=models.CASCADE)
#     part = models.ForeignKey('sparepart.SparePart', on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=0)