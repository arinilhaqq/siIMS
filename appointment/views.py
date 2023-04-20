from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from initialinspection.models import InitialInspection
from .models import Appointment, Pelanggan, Karyawan
from .forms import AppointmentForm

def is_authenticated(request):
    try:
        request.session['username']
        return True
    except:
        return False
    
def create_appointment(request):
    if is_authenticated(request):
        pelanggan = Pelanggan.objects.all()

        if request.method == 'POST':
            form = AppointmentForm(request.POST)

            if form.is_valid():
                appointment = form.save(commit=False)
                if appointment.teknisi:
                    appointment.status = 'On going'
                appointment.save()
                return redirect('/list-appointment/')
        else:
            form = AppointmentForm()
        
        teknisi = Karyawan.objects.filter(jabatan='Teknisi', kehadiran='Hadir',
                    appointment__teknisi__isnull=True) | Karyawan.objects.filter(jabatan='Teknisi',kehadiran='Hadir',
                    appointment__teknisi__isnull=False).exclude(appointment__status='On going')
        
        teknisi_dict = {}
        unique_teknisi = []
        for t in teknisi:
            if t not in teknisi_dict:
                teknisi_dict[t] = True
                unique_teknisi.append(t)

        context = {
            'listPelanggan': pelanggan,
            'listTeknisi': unique_teknisi,
            'form': form,
            'username': request.session['username'],
            'jabatan': request.session['jabatan']
        }
        return render(request, 'create-appointment.html', context)
    else:
        return HttpResponseRedirect("/login")

def list_appointment(request):
    initial_inspection = InitialInspection.objects.all()
    
    if is_authenticated(request):
        if request.session['jabatan'] != 'Teknisi':
            appointment = Appointment.objects.all()

            context = {
                'appointment': appointment,
                'username': request.session['username'],
                'jabatan': request.session['jabatan'],
                'initial': initial_inspection
            }

            return render(request, 'appointment-list.html', context)
        elif request.session['jabatan'] == 'Teknisi':
            appointment = Appointment.objects.filter(teknisi__nama_karyawan=request.session['nama_karyawan'])

            context = {
                'appointment': appointment,
                'username': request.session['username'],
                'jabatan': request.session['jabatan'],
            }

            return render(request, 'appointment-list.html', context)
        else:
            return HttpResponseRedirect ("/")
    else:
        return HttpResponseRedirect("/login")
    
def teknisi_finished_appointment(request, id):
    if is_authenticated(request):
        appoint_confirm = Appointment.objects.get(id=id)
        appoint_confirm.status = 'Finished'
        appoint_confirm.save()

        return redirect('/list-appointment/')
    else:
        return HttpResponseRedirect("/login")
