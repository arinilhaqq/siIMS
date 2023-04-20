from django import forms
from multiselectfield import MultiSelectFormField
from .models import InitialInspection, KONDISI_INTERIOR

class InitialInspectionForm(forms.ModelForm):
    class Meta:
        model = InitialInspection
        fields = '__all__'
