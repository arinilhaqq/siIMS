from django import forms
from pelanggan.models import Pelanggan

class PelangganForm(forms.ModelForm):
    class Meta:
        model = Pelanggan
        fields = ['nama_pelanggan',
                  'telepon_pelanggan',
                  'alamat_pelanggan',
                  'jenis_mobil',
                  'nama_mobil',
                  'nomor_pkb',
                  'nomor_polisi',
                  'email'
                  ]

class PelangganSearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=False)