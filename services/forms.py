from django import forms
from services.models import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['nama',
                  'harga',
                  'estimasi_pengerjaan',
<<<<<<< HEAD
                  'kebutuhan_spare_part',
                  'kuantitas_spare_part'
=======
                  'kebutuhan_spare_part'
>>>>>>> 79e180fa5d32da73d97f852db285b72c1061b136
                  ]
