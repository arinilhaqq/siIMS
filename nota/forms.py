from django import forms
from multiselectfield import MultiSelectFormField
from .models import NotaGabungan, NotaBarang

class NotaGabunganForms(forms.ModelForm):
    class Meta:
        model = NotaGabungan
        fields = ['keterangan_lain_lain',
                  'total_harga_lainlain'
                  ]

class NotaBarangForms(forms.ModelForm):
    class Meta:
        model = NotaBarang
        fields = ['petugas_gudang',
                  'petugas_bengkel'
                  ]                  