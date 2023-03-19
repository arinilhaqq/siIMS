from django import forms
from karyawan.models import Karyawan

class LoginForm(forms.Form) :
    username = forms.CharField(max_length = 50)
    password = forms.CharField(max_length = 50)
    # class Meta:
    #     model = Karyawan
    #     fields=[
    #         'username',
    #         'password'
    #     ]
    #     widgets = {
    #         'password': forms.PasswordInput()
    #     }