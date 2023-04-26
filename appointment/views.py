from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from initialinspection.models import InitialInspection
from appointment.models import Appointment
from .models import Pelanggan, Karyawan
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
            # print(request.POST)
            form = AppointmentForm(request.POST)
            # print(form)
            print(form.errors)

            if form.is_valid():
                appointment = form.save(commit=False)

                print(form.cleaned_data)
                teknisi = form.cleaned_data['teknisi']

                if teknisi:
                    appointment.teknisi = teknisi
                    appointment.status = 'On going'
                appointment.save()

                return redirect('/list-appointment/')
        else:
            form = AppointmentForm()

        # # Ambil semua teknisi
        # listTeknisi = Karyawan.objects.filter(jabatan='Teknisi', kehadiran='Hadir')
        
        # # Ambil semua appointment yang berjalan
        # listAppointment = Appointment.objects.all()
        # list_ongoing_Appoint = []

        # for appointment in listAppointment:
        #     if appointment.status == 'On going':
        #         list_ongoing_Appoint.append(appointment)

        # ongoingTeknisi = set()
        # finalTeknisi = set()

        # # Ambil teknisi yang punya appointment
        # for app in list_ongoing_Appoint:
        #     ongoingTeknisi.add(app.teknisi)

        # # Ambil teknisi yang gapunya appointment
        # for teknisi in listTeknisi:
        #     if teknisi not in ongoingTeknisi:
        #         finalTeknisi.add(teknisi)
        finalTeknisi = Karyawan.objects.filter(jabatan='Teknisi', kehadiran='Hadir').exclude(appointment__teknisi__isnull=False, appointment__status='On going')

        context = {
            'listPelanggan': pelanggan,
            'listTeknisi': finalTeknisi,
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

def update_appointment(request, id):
    if is_authenticated(request):
        appointment = Appointment.objects.get(id=id)
        finalTeknisi = Karyawan.objects.filter(jabatan='Teknisi', kehadiran='Hadir').exclude(appointment__teknisi__isnull=False, appointment__status='On going')
        response = {'appointment': appointment, 'username':request.session['username'], 'jabatan':request.session['jabatan'], 'listTeknisi': finalTeknisi}
        if request.method == 'POST':
            form = AppointmentForm(request.POST, instance=appointment)
            if form.is_valid():
                appointment = form.save(commit=False) 
                teknisi_id = request.POST.get('teknisi', None)
                keluhan = request.POST.get('keluhan', None)

                if teknisi_id:
                    teknisi = Karyawan.objects.get(id=teknisi_id)
                    appointment.teknisi = teknisi
                    appointment.status = 'On going'
                
                if keluhan:
                    appointment.keluhan = keluhan
            appointment.save()
            return redirect('/list-appointment/')
        return render(request, "update-appointment.html", response)
    else:
        return HttpResponseRedirect("/login")
