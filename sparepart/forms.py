from django import forms
from sparepart.models import SparePart
from services.models import Service

class SparePartForm(forms.ModelForm):

    class Meta:
        model = SparePart
        fields = ['nama',
                  'variasi',
                  'harga',
                  'stok',
                  'services'
                  ]
        widgets = {
            'services': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['services'].queryset = Service.objects.all()
