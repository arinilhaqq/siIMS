from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from initialinspection.models import InitialInspection
from finalinspection.models import FinalInspection
from sparepart.models import SparePart
from appointment.models import Appointment, AppointmentService
from .models import Pelanggan, Karyawan, Service
from .forms import AppointmentForm, AppointmentSearchForm, AppointmentSortForm
from django.db import connection

def is_authenticated(request):
    try:
        request.session['username']
        return True
    except:
        return False

def create_appointment(request):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan' and request.session['jabatan'] !='Inventori' and request.session['jabatan'] !='Teknisi':
            pelanggan = Pelanggan.objects.all()

            if request.method == 'POST':
                form = AppointmentForm(request.POST)
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

            listTeknisi = Karyawan.objects.filter(jabatan='Teknisi', kehadiran='Hadir').exclude(appointment__teknisi__isnull=False, appointment__status='On going').exclude(appointment__teknisi__isnull=False, appointment__status='Approved')
            
            context = {
                'listPelanggan': pelanggan,
                'listTeknisi': listTeknisi,
                'form': form,
                'username': request.session['username'],
                'jabatan': request.session['jabatan']
            }
            return render(request, 'create-appointment.html', context)
        else:
            return HttpResponseRedirect ("/")
    else:
        return HttpResponseRedirect("/login")
    
def list_appointment(request):
    # Initial Inspection
    initial_inspection = InitialInspection.objects.all()
    appointment_initial_inspection = []

    for init in initial_inspection:
        appointment_initial_inspection.append(init.appointment)

    # Final Inspection
    final_inspection = FinalInspection.objects.all()
    appointment_final_inspection = []

    for final in final_inspection:
        appointment_final_inspection.append(final.appointment)

    if is_authenticated(request):
        if request.session['jabatan'] != 'Teknisi':
            appointment = Appointment.objects.all()

            form = AppointmentSearchForm(request.GET)
            form_sort = AppointmentSortForm(request.GET)

            context = {
                'appointment': appointment,
                'username': request.session['username'],
                'jabatan': request.session['jabatan'],
                'initial': initial_inspection,
                'final': final_inspection,
                'appointment_initial_inspection': appointment_initial_inspection,
                'appointment_final_inspection': appointment_final_inspection,
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
                'initial': initial_inspection,
                'final': final_inspection,
                'appointment_initial_inspection': appointment_initial_inspection,
                'appointment_final_inspection': appointment_final_inspection,
            }

            return render(request, 'appointment-list.html', context)
        
        elif request.session['jabatan'] == 'Teknisi':
            appointment = Appointment.objects.filter(teknisi__nama_karyawan=request.session['nama_karyawan'])

            form = AppointmentSearchForm(request.GET)
            form_sort = AppointmentSortForm(request.GET)

            context = {
                'appointment': appointment,
                'username': request.session['username'],
                'jabatan': request.session['jabatan'],
                'initial': initial_inspection,
                'final': final_inspection,
                'appointment_initial_inspection': appointment_initial_inspection,
                'appointment_final_inspection': appointment_final_inspection,
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
                'initial': initial_inspection,
                'final': final_inspection,
                'appointment_initial_inspection': appointment_initial_inspection,
                'appointment_final_inspection': appointment_final_inspection,
            }        

            return render(request, 'appointment-list.html', context)
        else:
            return HttpResponseRedirect ("/")
    else:
        return HttpResponseRedirect("/login")

    
def teknisi_finished_appointment(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan' and request.session['jabatan'] !='Inventori':
            appoint_confirm = Appointment.objects.get(id=id)
            appoint_confirm.status = 'Finished'
            appoint_confirm.save()

            return redirect('/list-appointment/')
        else:
            return HttpResponseRedirect ("/")
    else:
        return HttpResponseRedirect("/login")

def update_appointment(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan' and request.session['jabatan'] !='Inventori':
            appointment = Appointment.objects.get(id=id)
            finalTeknisi = Karyawan.objects.filter(jabatan='Teknisi', kehadiran='Hadir').exclude(appointment__teknisi__isnull=False, appointment__status='On going').exclude(appointment__teknisi__isnull=False, appointment__status='Approved')
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
        service_ids = [item['id'] for item in services]

        spare_part_ids = [] 
        sparepart_kuantitas = {}

        status_sparepart = {}

        appointment_service = AppointmentService.objects.all()
        
        all_cukup = True
        
        for service_id in service_ids:
            cursor = connection.cursor()
            cursor.execute("SET search_path TO public")
            cursor.execute(
                'SELECT * FROM public."services_service_kebutuhan_spare_part" WHERE '
                '"services_service_kebutuhan_spare_part"."service_id"=%s',
                [service_id])
            rows = cursor.fetchall()
            # print(rows)
            for j in range(len(rows)):
                id_sparepart = rows[j][2]
                kuantitas_sparepart = rows[j][3]

                if kuantitas_sparepart == None:
                    kuantitas_sparepart = 0

                spare_part_ids.append(rows[j][2])
                sparepart_ybs = SparePart.objects.get(id=id_sparepart)
                kuantitas_ybs = sparepart_ybs.stok
                
                if kuantitas_ybs >= kuantitas_sparepart:
                    if (service_id not in status_sparepart or status_sparepart[service_id] != "Tidak Cukup"):
                        status_sparepart[service_id] = "Cukup"
                else:
                    status_sparepart[service_id] = "Tidak Cukup"
                print(status_sparepart)

                
        list_status = list(status_sparepart.values())
        for status in list_status:
            if status == "Tidak Cukup":
                all_cukup = False
                break

        context = {
            'appointment': appointment,
            'services': services,
            # 'status_sparepart': status_sparepart,
            # 'all_cukup': all_cukup,
            'appointment_service': appointment_service,
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
        service_ids = [item['id'] for item in services]

        total_harga_service = {}
        total_lama_pengerjaan = {
            'Bulan': 0,
            'Minggu': 0,
            'Hari': 0,
            'Jam': 0,
            'Menit': 0,
        }

        for service_id in service_ids:
            cursor = connection.cursor()
            cursor.execute("SET search_path TO public")
            cursor.execute(
                'SELECT * FROM public."services_service_kebutuhan_spare_part" WHERE '
                '"services_service_kebutuhan_spare_part"."service_id"=%s',
                [service_id])
            rows = cursor.fetchall()
            print(rows)
            for j in range(len(rows)):
                id_service = rows[j][1]
                id_sparepart = rows[j][2]
                kuantitas_sparepart = rows[j][3]
                if kuantitas_sparepart == None:
                    kuantitas_sparepart = 0
                if id_service == service_id:
                    sparepart = SparePart.objects.get(id=id_sparepart)
                    servis = Service.objects.get(id=service_id)
                    harga = sparepart.harga
                    total = harga*kuantitas_sparepart
                    total += servis.harga
                    total_harga_service[service_id] = total
            
            serv = Service.objects.get(id=service_id)
            if serv.satuan_waktu == 'Bulan':
                total_lama_pengerjaan['Bulan'] += serv.jumlah_estimasi_pengerjaan
            elif serv.satuan_waktu == 'Minggu':
                total_lama_pengerjaan['Minggu'] += serv.jumlah_estimasi_pengerjaan
            elif serv.satuan_waktu == 'Hari':
                total_lama_pengerjaan['Hari'] += serv.jumlah_estimasi_pengerjaan
            elif serv.satuan_waktu == 'Jam':
                total_lama_pengerjaan['Jam'] += serv.jumlah_estimasi_pengerjaan
            else:
                total_lama_pengerjaan['Menit'] += serv.jumlah_estimasi_pengerjaan
                
        list_harga = list(total_harga_service.values())
        total_harga = 0
        for price in list_harga:
            total_harga += price
        
        total_lama = ""

        for key, value in total_lama_pengerjaan.items():
            if value > 0:
                total_lama += "{} {} ".format(value, key)

        context = {
            'appointment': appointment,
            'services': services,
            'total_harga_service': total_harga_service,
            'total_harga': total_harga,
            'total_lama': total_lama,
            'username': request.session['username'],
            'jabatan': request.session['jabatan'],
        }
        return render(request, 'estimasi-appointment.html', context)
    else:
        return HttpResponseRedirect("/login")
    
def cancel_appointment(request, id):
    if is_authenticated(request):
        appoint_cancel = Appointment.objects.get(id=id)
        appoint_cancel.status = 'Canceled'
        appoint_cancel.save()

        return redirect('/list-appointment/')
    else:
        return HttpResponseRedirect("/login")
    
def approve_appointment(request, id):
    if is_authenticated(request):
        appointment = Appointment.objects.get(id=id)

        appointment.status = 'Approved'

        appointment.save()

        services = appointment.services.all().values()
        
        service_ids = [item['id'] for item in services]

        for service_id in service_ids:
            cursor = connection.cursor()
            cursor.execute("SET search_path TO public")
            cursor.execute(
                'SELECT * FROM public."services_service_kebutuhan_spare_part" WHERE '
                '"services_service_kebutuhan_spare_part"."service_id"=%s',
                [service_id])
            rows = cursor.fetchall()
            print(rows)

            for j in range(len(rows)):
                id_service = rows[j][1]
                id_sparepart = rows[j][2]
                kuantitas_sparepart = rows[j][3]
                sparepart = SparePart.objects.get(id=id_sparepart)

                if kuantitas_sparepart == None:
                    kuantitas_sparepart = 0

                sparepart.stok -= kuantitas_sparepart
                sparepart.save()

        return redirect('/list-appointment/')
    else:
        return HttpResponseRedirect("/login")
    
def delete_appointment(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan' and request.session['jabatan'] !='Inventori'and request.session['jabatan'] !='Teknisi':
            appointment_by_id = Appointment.objects.get(id=id)

            if (appointment_by_id.status == 'Not Ready' or appointment_by_id.status == 'Canceled'):
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
        service_ids = [item['id'] for item in services]

        spare_part_ids = [] 
        sparepart_kuantitas = {}

        status_sparepart = {}

        all_cukup = True
        
        for service_id in service_ids:
            cursor = connection.cursor()
            cursor.execute("SET search_path TO public")
            cursor.execute(
                'SELECT * FROM public."services_service_kebutuhan_spare_part" WHERE '
                '"services_service_kebutuhan_spare_part"."service_id"=%s',
                [service_id])
            rows = cursor.fetchall()
            print(rows)
            for j in range(len(rows)):
                id_sparepart = rows[j][2]
                kuantitas_sparepart = rows[j][3]
                if kuantitas_sparepart == None:
                    kuantitas_sparepart = 0
                spare_part_ids.append(rows[j][2])
                sparepart_ybs = SparePart.objects.get(id=id_sparepart)
                kuantitas_ybs = sparepart_ybs.stok
                if kuantitas_ybs >= kuantitas_sparepart:
                    status_sparepart[service_id] = "Cukup"
                else:
                    status_sparepart[service_id] = "Tidak Cukup"

                
        list_status = list(status_sparepart.values())
        for status in list_status:
            if status == "Tidak Cukup":
                all_cukup = False
                break

        print(services)
        print(service_ids)
        print(spare_part_ids)
        print(sparepart_kuantitas)
        print(status_sparepart)

        context = {
            'appointment': appointment,
            'services': services,
            'status_sparepart': status_sparepart,
            'all_cukup': all_cukup,
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
        service_ids = [item['id'] for item in services]

        total_harga_service = {}
        total_lama_pengerjaan = {
            'Bulan': 0,
            'Minggu': 0,
            'Hari': 0,
            'Jam': 0,
            'Menit': 0,
        }

        for service_id in service_ids:
            cursor = connection.cursor()
            cursor.execute("SET search_path TO public")
            cursor.execute(
                'SELECT * FROM public."services_service_kebutuhan_spare_part" WHERE '
                '"services_service_kebutuhan_spare_part"."service_id"=%s',
                [service_id])
            rows = cursor.fetchall()
            print(rows)
            for j in range(len(rows)):
                id_service = rows[j][1]
                id_sparepart = rows[j][2]
                kuantitas_sparepart = rows[j][3]
                if kuantitas_sparepart == None:
                    kuantitas_sparepart = 0
                if id_service == service_id:
                    sparepart = SparePart.objects.get(id=id_sparepart)
                    servis = Service.objects.get(id=service_id)
                    harga = sparepart.harga
                    total = harga*kuantitas_sparepart
                    total += servis.harga
                    total_harga_service[service_id] = total
            
            serv = Service.objects.get(id=service_id)
            if serv.satuan_waktu == 'Bulan':
                total_lama_pengerjaan['Bulan'] += serv.jumlah_estimasi_pengerjaan
            elif serv.satuan_waktu == 'Minggu':
                total_lama_pengerjaan['Minggu'] += serv.jumlah_estimasi_pengerjaan
            elif serv.satuan_waktu == 'Hari':
                total_lama_pengerjaan['Hari'] += serv.jumlah_estimasi_pengerjaan
            elif serv.satuan_waktu == 'Jam':
                total_lama_pengerjaan['Jam'] += serv.jumlah_estimasi_pengerjaan
            else:
                total_lama_pengerjaan['Menit'] += serv.jumlah_estimasi_pengerjaan
                
        list_harga = list(total_harga_service.values())
        total_harga = 0
        for price in list_harga:
            total_harga += price
        
        total_lama = ""

        for key, value in total_lama_pengerjaan.items():
            if value > 0:
                total_lama += "{} {} ".format(value, key)

        context = {
            'appointment': appointment,
            'services': services,
            'total_harga_service': total_harga_service,
            'total_harga': total_harga,
            'total_lama': total_lama,
            'username': request.session['username'],
            'jabatan': request.session['jabatan'],
        }
        return render(request, 'estimasi-appointment.html', context)
    else:
        return HttpResponseRedirect("/login")
    
def cancel_appointment(request, id):
    if is_authenticated(request):
        appoint_cancel = Appointment.objects.get(id=id)
        appoint_cancel.status = 'Canceled'
        appoint_cancel.save()

        return redirect('/list-appointment/')
    else:
        return HttpResponseRedirect("/login")
    
def approve_appointment(request, id):
    if is_authenticated(request):
        appointment = Appointment.objects.get(id=id)

        appointment.status = 'Approved'

        appointment.save()

        services = appointment.services.all().values()
        
        service_ids = [item['id'] for item in services]

        for service_id in service_ids:
            cursor = connection.cursor()
            cursor.execute("SET search_path TO public")
            cursor.execute(
                'SELECT * FROM public."services_service_kebutuhan_spare_part" WHERE '
                '"services_service_kebutuhan_spare_part"."service_id"=%s',
                [service_id])
            rows = cursor.fetchall()
            print(rows)

            for j in range(len(rows)):
                id_service = rows[j][1]
                id_sparepart = rows[j][2]
                kuantitas_sparepart = rows[j][3]
                if (kuantitas_sparepart == None):
                    kuantitas_sparepart = 0
                sparepart = SparePart.objects.get(id=id_sparepart)
                sparepart.stok -= kuantitas_sparepart
                sparepart.save()

        return redirect('/list-appointment/')
    else:
        return HttpResponseRedirect("/login")