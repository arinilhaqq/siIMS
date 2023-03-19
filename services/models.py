from django.db import models
<<<<<<< HEAD
from multiselectfield import MultiSelectField
# from jsonfield import JSONField
=======

from multiselectfield import MultiSelectField
>>>>>>> 79e180fa5d32da73d97f852db285b72c1061b136


MY_CHOICES2 = ((1, 'Baut'),
               (2, 'Oli'),
               (3, 'Besi'),
               (4, 'Bamper'),
               (5, 'Ban'))

class Service(models.Model):
    nama = models.CharField(max_length=30)
<<<<<<< HEAD
    harga = models.IntegerField()
    estimasi_pengerjaan = models.CharField(max_length=10)
    kebutuhan_spare_part = MultiSelectField(choices=MY_CHOICES2, default='')
    kuantitas_spare_part = models.CharField(max_length=255, default='')

=======
    harga = models.CharField(max_length=10)
    estimasi_pengerjaan = models.CharField(max_length=10)
    kebutuhan_spare_part = MultiSelectField(choices=MY_CHOICES2, default='')
>>>>>>> 79e180fa5d32da73d97f852db285b72c1061b136
