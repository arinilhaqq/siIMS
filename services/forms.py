from django import forms
from services.models import Service
# from services.models import ServicePart
from sparepart.models import SparePart

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['nama',
                  'harga',
                  'jumlah_estimasi_pengerjaan',
                  'satuan_waktu',
                  'kebutuhan_spare_part'
                  ]
        widgets = {
            'kebutuhan_spare_part': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['kebutuhan_spare_part'].queryset = SparePart.objects.all()

class ServiceSearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=False)

URUTAN_CHOICES = (
    ('Termahal', 'Termahal'),
    ('Termurah', 'Termurah'),
)

class ServiceSortForm(forms.Form):
    pilihan = forms.ChoiceField(choices=URUTAN_CHOICES, required=False)

class SparePartItemForm(forms.Form):
    quantity = forms.IntegerField()
