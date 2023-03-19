from django.db import models
from multiselectfield import MultiSelectField
# from jsonfield import JSONField


MY_CHOICES2 = ((1, 'Baut'),
               (2, 'Oli'),
               (3, 'Besi'),
               (4, 'Bamper'),
               (5, 'Ban'))

class Service(models.Model):
    nama = models.CharField(max_length=30)
    harga = models.IntegerField()
    estimasi_pengerjaan = models.CharField(max_length=10)
    kebutuhan_spare_part = MultiSelectField(choices=MY_CHOICES2, default='')
    kuantitas_spare_part = models.CharField(max_length=255, default='')

