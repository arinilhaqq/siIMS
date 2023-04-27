from django import forms
from karyawan.models import Karyawan

class KaryawanForm(forms.ModelForm):
    class Meta:
        model = Karyawan
    class Meta:
        model = Karyawan
        fields = ['nama_karyawan',
                  'telepon_karyawan',
                  'alamat_karyawan',
                  'jabatan',
                  'kehadiran',
                  'email',
                  'username',
                  'password'
                  ]

class KaryawanSearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=False)

URUTAN_CHOICES = (
    ('Terbaru', 'Terbaru'),
    ('Terlama', 'Terlama'),
)

class KaryawanSortForm(forms.Form):
    pilihan = forms.ChoiceField(choices=URUTAN_CHOICES, required=False)