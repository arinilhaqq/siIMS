from django import forms
from kendala.models import Kendala

class KendalaForm(forms.ModelForm):
    class Meta:
        model = Kendala
    class Meta:
        model = Kendala
        fields = ['appointment_service',
                  'deskripsi',
                  'status',
                  'service',
                  'jumlah_estimasi_pengerjaan',
                  'satuan_waktu',
                  ]