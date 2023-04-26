import datetime
from django import forms
from .models import Appointment, Pelanggan, Karyawan
from django.db.models import Q

class CustomerModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.nama_pelanggan} ({obj.nomor_polisi})"
    
class TeknisiModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.nama_karyawan}"
    
class AppointmentForm(forms.ModelForm):
    pelanggan = CustomerModelChoiceField(queryset=Pelanggan.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    
    teknisi = TeknisiModelChoiceField(queryset=Karyawan.objects.filter(jabatan='Teknisi', kehadiran='Hadir')
        .exclude(appointment__teknisi__isnull=False, appointment__status='On going'), required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Appointment
        fields = ['pelanggan', 'keluhan']
        
    def save(self, commit=True):
        appointment = super(AppointmentForm, self).save(commit=False)
        appointment.date = datetime.datetime.today().date()
        appointment.time = datetime.datetime.now().time()
        
        if commit:
            appointment.save()
            
        return appointment