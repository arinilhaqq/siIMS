from django import forms
from multiselectfield import MultiSelectFormField
from .models import FinalInspection, KONDISI_INTERIOR

class FinalInspectionForm(forms.ModelForm):
    class Meta:
        model = FinalInspection
        fields = '__all__'