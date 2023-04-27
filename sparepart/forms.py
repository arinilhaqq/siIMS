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

class SparepartSearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=False)

URUTAN_CHOICES = (
    ('Terbanyak', 'Terbanyak'),
    ('Terdikit', 'Terdikit'),
)

class SparepartSortForm(forms.Form):
    pilihan = forms.ChoiceField(choices=URUTAN_CHOICES, required=False)