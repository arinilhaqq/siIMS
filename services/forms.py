from django import forms
from services.models import Service
# from services.models import ServicePart
from sparepart.models import SparePart

class ServiceForm(forms.ModelForm):

    quantities = forms.CharField()

    class Meta:
        model = Service
        fields = ['nama',
                  'harga',
                  'jumlah_estimasi_pengerjaan',
                  'satuan_waktu',
                  'kebutuhan_spare_part'
                  ]
        widgets = {
            'kebutuhan_spare_part': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['kebutuhan_spare_part'].queryset = SparePart.objects.all()

class SparePartItemForm(forms.Form):
    quantity = forms.IntegerField()
