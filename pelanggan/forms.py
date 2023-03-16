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
