from django import forms
from multiselectfield import MultiSelectFormField
from .models import Nota

class FinalInspectionForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = '__all__'