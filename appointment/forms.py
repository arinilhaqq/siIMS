import datetime
from django import forms
from .models import Appointment, Pelanggan, Karyawan
from django.db.models import Q

class CustomerModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.nama_pelanggan} ({obj.nomor_polisi})"
    
class AppointmentForm(forms.ModelForm):
    pelanggan = CustomerModelChoiceField(queryset=Pelanggan.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    teknisi = forms.ModelChoiceField(queryset=Karyawan.objects.filter(jabatan='Teknisi', kehadiran='Hadir',
                appointment__teknisi__isnull=True) | Karyawan.objects.filter(jabatan='Teknisi',kehadiran='Hadir',
                appointment__teknisi__isnull=False).exclude(appointment__status='On going'), required=False,
    )
    
    class Meta:
        model = Appointment
        fields = ['pelanggan', 'keluhan', 'teknisi']
        
    def save(self, commit=True):
        appointment = super(AppointmentForm, self).save(commit=False)
        appointment.date = datetime.datetime.today().date()
        appointment.time = datetime.datetime.now().time()
        
        if commit:
            appointment.save()
            
        return appointment