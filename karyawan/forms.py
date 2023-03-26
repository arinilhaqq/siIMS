from django import forms
from karyawan.models import Karyawan

class KaryawanForm(forms.ModelForm):
    class Meta:
        model = Karyawan
        fields = ['nama_karyawan',
                  'telepon_karyawan',
                  'alamat_karyawan',
                  'jabatan',
                  'kehadiran',
                  'total_keaktifan',
                  'email',
                  'username',
                  'password'
                  ]
