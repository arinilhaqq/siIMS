from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from initialinspection.models import InitialInspection
from sparepart.models import SparePart
from .models import Appointment, Pelanggan, Karyawan, Service
from .forms import AppointmentForm, AppointmentSearchForm, AppointmentSortForm

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

            form = AppointmentSearchForm(request.GET)
            form_sort = AppointmentSortForm(request.GET)

            context = {
                'appointment': appointment,
                'username': request.session['username'],
                'jabatan': request.session['jabatan'],
                'initial': initial_inspection
            }

            if form.is_valid():
                search_query = form.cleaned_data.get('search_query')
                
                if search_query:
                    appointment = appointment.filter(pelanggan__nama_pelanggan__icontains=search_query) | appointment.filter(status__icontains=search_query)

            if form_sort.is_valid():
                pilihan = form_sort.cleaned_data.get('pilihan')

                if pilihan:
                    if pilihan == 'Terbaru':
                        appointment = appointment.order_by("-id")
                    elif pilihan == 'Terlama':
                        appointment = appointment.order_by("id")

            context = {
                "form": form,
                'form_sort': form_sort,
                'appointment': appointment,
                'username': request.session['username'],
                'jabatan': request.session['jabatan'],
                'initial': initial_inspection
            }
            
            return render(request, 'appointment-list.html', context)
        
            
        elif request.session['jabatan'] == 'Teknisi':
            appointment = Appointment.objects.filter(teknisi__nama_karyawan=request.session['nama_karyawan'])

            form = AppointmentSearchForm(request.GET)

            context = {
                'appointment': appointment,
                'username': request.session['username'],
                'jabatan': request.session['jabatan'],
            }

            if form.is_valid():
                search_query = form.cleaned_data.get('search_query')
                
                if search_query:
                    appointment = appointment.filter(pelanggan__nama_pelanggan__icontains=search_query) | appointment.filter(status__icontains=search_query)
                    
            context = {
                "form": form,
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
    

def delete_appointment(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan' and request.session['jabatan'] !='Inventori'and request.session['jabatan'] !='Teknisi':
            appointment_by_id = Appointment.objects.get(id=id)
            appointment_by_id.delete()

            return redirect('/list-appointment/')
        else:
            return HttpResponseRedirect ("/")
    else:
            return HttpResponseRedirect("/login")
    
def possible_service(request, id):
    if is_authenticated(request):
        appointment = get_object_or_404(Appointment, pk=id)
        # appointment = Appointment.objects.get(id=id)
        all_service = Service.objects.all()

        if request.method == 'POST':
            print(id)
            service_ids = request.POST.getlist('services')
            print(service_ids)
            services = Service.objects.filter(id__in=service_ids)
            appointment.services.set(services)
            return redirect(f"/service-appointment/{id}")
        context = {
            'appointment': appointment,
            'listservice': all_service,
            'username': request.session['username'],
            'jabatan': request.session['jabatan'],
        }

        return  render(request, 'service-possible.html', context)
    else:
        return HttpResponseRedirect("/login")
    
def list_service_appointment(request, id):
    if is_authenticated(request):
        appointment = Appointment.objects.get(id=id)
        # appointment = Appointment.objects.prefetch_related('services').get(id=id)
        services = appointment.services.all().values()
        services_cek = appointment.services.all()
        print(services)
        # for service in services:
        #     kuantitas = services_cek.
        all_sparepart = SparePart.objects.all()

        context = {
            'appointment': appointment,
            'services': services,
            'username': request.session['username'],
            'jabatan': request.session['jabatan'],
        }
        return render(request, 'service-appointment-list.html', context)
    else:
        return HttpResponseRedirect("/login")

def estimasi_appointment(request, id):
    if is_authenticated(request):
        appointment = Appointment.objects.get(id=id)
        services = appointment.services.all().values()
        total_harga = 0
        for service in services:
            total_harga += service['harga']
        context = {
            'appointment': appointment,
            'services': services,
            'total_harga': total_harga,
            'username': request.session['username'],
            'jabatan': request.session['jabatan'],
        }
        return render(request, 'estimasi-appointment.html', context)
    else:
        return HttpResponseRedirect("/login")