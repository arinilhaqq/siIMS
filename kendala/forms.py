from django import forms
from kendala.models import Kendala

class KendalaForm(forms.ModelForm):
    class Meta:
        model = Kendala
    class Meta:
        model = Kendala
        fields = '__all__'