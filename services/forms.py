from django import forms
from services.models import Service
from sparepart.models import SparePart

class ServiceForm(forms.ModelForm):

    quantities = forms.CharField()

    class Meta:
        model = Service
        fields = ['nama',
                  'harga',
                  'jumlah_estimasi_pengerjaan',
                  'satuan_waktu',
                  'kebutuhan_spare_parts',
                  'quantities'
                  ]
        widgets = {
            'kebutuhan_spare_parts': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['kebutuhan_spare_parts'].queryset = SparePart.objects.all()

    def save(self, commit=True):
        service = super(ServiceForm, self).save(commit=False)
        if commit:
            service.save()
        for part, quantity in zip(self.cleaned_data['kebutuhan_spare_parts'], self.cleaned_data['quantities'].split(',')):
            ServicePart.objects.create(service=service, part=part, quantity=int(quantity))
        return service


