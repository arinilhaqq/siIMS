from django import forms
# from .models import Karyawan
from karyawan.models import Karyawan

class LoginForm(forms.ModelForm) :
    # username = forms.CharField(max_length = 50)
    # password = forms.CharField(max_length = 50)
    class Meta:
        model = Karyawan
        fields=[
            'username',
            'password'
        ]
        widgets = {
            'password': forms.PasswordInput()
        }

