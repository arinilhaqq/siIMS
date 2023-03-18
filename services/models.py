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
    harga = models.CharField(max_length=10)
    estimasi_pengerjaan = models.CharField(max_length=10)
    kebutuhan_spare_part = MultiSelectField(choices=MY_CHOICES2, default='')
    kuantitas_spare_part = models.CharField(max_length=255, default='')
    # kuantitas_spare_part = forms.IntegerField(min_value=1, initial=1, widget=forms.NumberInput(attrs={'min': '1', 'max': '100'}))

