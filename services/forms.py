from django import forms
from services.models import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['nama',
                  'harga',
                  'estimasi_pengerjaan',
                  'kebutuhan_spare_part'
                  ]
