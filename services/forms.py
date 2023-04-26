from django import forms
from services.models import Service
<<<<<<< HEAD
=======
# from services.models import ServicePart
>>>>>>> a8a6b82b05b48c3ccf85412e2a6f702ae9c1ebd6
from sparepart.models import SparePart

class ServiceForm(forms.ModelForm):

    quantities = forms.CharField()

    class Meta:
        model = Service
        fields = ['nama',
                  'harga',
                  'jumlah_estimasi_pengerjaan',
                  'satuan_waktu',
<<<<<<< HEAD
                  'kebutuhan_spare_parts',
                  'quantities'
                  ]
        widgets = {
            'kebutuhan_spare_parts': forms.CheckboxSelectMultiple()
=======
                  'kebutuhan_spare_part'
                  ]
        widgets = {
            'kebutuhan_spare_part': forms.CheckboxSelectMultiple()
>>>>>>> a8a6b82b05b48c3ccf85412e2a6f702ae9c1ebd6
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
<<<<<<< HEAD
        self.fields['kebutuhan_spare_parts'].queryset = SparePart.objects.all()

    def save(self, commit=True):
        service = super(ServiceForm, self).save(commit=False)
        if commit:
            service.save()
        for part, quantity in zip(self.cleaned_data['kebutuhan_spare_parts'], self.cleaned_data['quantities'].split(',')):
            ServicePart.objects.create(service=service, part=part, quantity=int(quantity))
        return service


=======
        self.fields['kebutuhan_spare_part'].queryset = SparePart.objects.all()

class SparePartItemForm(forms.Form):
    quantity = forms.IntegerField()
>>>>>>> a8a6b82b05b48c3ccf85412e2a6f702ae9c1ebd6
