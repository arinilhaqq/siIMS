import calendar
import json
from services.models import Service
from appointment.models import AppointmentService
from sparepart.models import SparePart
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from appointment.models import Appointment
from karyawan.models import Karyawan
from django.contrib.auth import update_session_auth_hash
from django.db import connection
from django.db.models import Count
from collections import Counter

def is_authenticated(request):
    try:
        request.session['username']
        return True
    except:
        return False

def homepage(request):
    print(is_authenticated)
    if is_authenticated(request):
        top_karyawan = Appointment.objects \
                    .values('teknisi__id') \
                    .annotate(count=Count('id')) 
        
        print(top_karyawan)

        karyawan_keaktifan = {}
        for karyawan in top_karyawan:
            karyawan_keaktifan[karyawan['teknisi__id']] = karyawan['count']

        print(karyawan_keaktifan)
        for idk, count in karyawan_keaktifan.items():
            karyawan = Karyawan.objects.get(id=idk)
            karyawan.total_keaktifan = count
            karyawan.save()
            
        context = {}
        context['nama_karyawan'] = request.session['nama_karyawan']
        context['username'] = request.session['username']
        if request.session['jabatan'] =='Admin'| request.session['jabatan'] =='Owner'|request.session['jabatan'] =='Akuntan'|request.session['jabatan'] =='Inventori'|request.session['jabatan'] =='Teknisi'|request.session['jabatan'] =='Service Advisor':
            return render(request, 'homepage.html', context)
    else:
        return HttpResponseRedirect("/login")


def change_password(request):
    context = {}
    # karyawan = Karyawan.objects.get(username=request.session['username'])
    # ch = Karyawan.objects.filter(user__id=request.session['id'])
    # if len(ch)>0:
    #     data = Karyawan.objects.get(user__id=request.session['id'])
    #     context["data"] = data
    context['username'] = request.session['username']
    context['jabatan'] = request.session['jabatan']
    
    if request.method=="POST":
        current = request.POST["cpwd"]
        new_pas = request.POST["npwd"]
        
        user = Karyawan.objects.get(username=request.session["username"])
        un = user.username
        if request.session["password"] == current:
            user.password = new_pas
            user.save()
            context["msz"] = "Password Changed Successfully!!!"
            context["col"] = "alert-success"
            user = Karyawan.objects.get(username=un)
            update_session_auth_hash(request, user)
            return redirect('/')
        else:
            context["msz"] = "Incorrect Current Password"
            context["col"] = "alert-danger"
    return render(request,"change-password.html",context)

def update_password(request, username):
    context= {}
    cursor = connection.cursor()
    if request.method=="POST":
        new_pas = request.POST["npwd"]
        cursor.execute("SET search_path TO public")
        cursor.execute('SELECT username FROM public."karyawan_karyawan" WHERE "karyawan_karyawan"."username"=username')
        user = Karyawan.objects.get(username=username)
        un = user.username
        user.password = new_pas
        user.save()
        context["msz"] = "Password Updated Successfully!!!"
        context["col"] = "alert-success"
        user = Karyawan.objects.get(username=un)
        # login(request,user)
        # update_session_auth_hash(request, user)
        request.session.clear()
        return redirect('/login')
    return render(request,"update-password.html",context)

def dashboard(request):
    if is_authenticated(request):
        context= {
            'username': request.session['username'],
            'jabatan': request.session['jabatan'],
        }
        return render(request, 'dashboard.html', context)
    else:
        return HttpResponseRedirect("/login")

def appointment_chart_date(request):
    if is_authenticated(request):
        if request.session['jabatan'] !='Inventori' and request.session['jabatan'] !='Teknisi':
            appointments = Appointment.objects.values('date').annotate(count=Count('date')).order_by('-date')

            labels = []
            data = []
            for appointment in appointments:
                labels.append(appointment['date'].strftime('%Y-%m-%d'))
                data.append(appointment['count'])

            # Serialize the data to JSON format
            labels_json = json.dumps(labels)
            data_json = json.dumps(data)

            context = {
                'labels': labels_json,
                'data': data_json,
                'username': request.session['username'],
                'jabatan': request.session['jabatan'],
            }

            return render(request, 'appointment-by-date.html', context)
        else:
                return HttpResponseRedirect ("/")
    else:
        return HttpResponseRedirect("/login")

def appointment_chart_week(request):
    if is_authenticated(request):
        if request.session['jabatan'] !='Inventori' and request.session['jabatan'] !='Teknisi':
            appointments = Appointment.objects.extra({'week': "EXTRACT(WEEK FROM date)"}).values('week').annotate(count=Count('id')).order_by('-week')

            labels = []
            data = []
            for appointment in appointments:
                week = appointment['week']
                labels.append(f"Week {week}")
                data.append(appointment['count'])

            # Serialize the data to JSON format
            labels_json = json.dumps(labels)
            data_json = json.dumps(data)

            context = {
                'labels': labels_json,
                'data': data_json,
                'username': request.session['username'],
                'jabatan': request.session['jabatan'],
            }

            return render(request, 'appointment-by-week.html', context)
        else:
            return HttpResponseRedirect ("/")
    else:
        return HttpResponseRedirect("/login")

def appointment_chart_month(request):
    if is_authenticated(request):
        if request.session['jabatan'] !='Inventori' and request.session['jabatan'] !='Teknisi':
            appointments = Appointment.objects.extra({'month': "EXTRACT(month FROM date)", 'year': "EXTRACT(year FROM date)"}) \
                .values('month', 'year').annotate(count=Count('id')).order_by('-year', '-month')

            labels = []
            data = []
            for appointment in appointments:
                month = appointment['month']
                year = appointment['year']
                month_name = calendar.month_name[int(month)]
                label = f"{month_name} {year}"
                labels.append(label)
                data.append(appointment['count'])

            # Serialize the data to JSON format
            labels_json = json.dumps(labels)
            data_json = json.dumps(data)

            context = {
                'labels': labels_json,
                'data': data_json,
                'username': request.session['username'],
                'jabatan': request.session['jabatan'],
            }

            return render(request, 'appointment-by-month.html', context)
        else:
            return HttpResponseRedirect ("/")
    else:
        return HttpResponseRedirect("/login")

def appointment_chart_top_customers(request):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan' and request.session['jabatan'] !='Inventori' and request.session['jabatan'] !='Teknisi':
            num_top_customers = request.GET.get('num_top_customers', 5)
            print(num_top_customers)
            try:
                num_top_customers = int(num_top_customers)
            except ValueError:
                num_top_customers = 5  

            top_customers = Appointment.objects \
                .values('pelanggan__nama_pelanggan') \
                .annotate(count=Count('id')) \
                .order_by('-count')[:num_top_customers]

            # print(len(top_customers))
            # Test case
            warning_text= ''
            if (len(top_customers) < num_top_customers):
                warning_text = 'Data top ' + str(num_top_customers) + ' loyalitas customer yang ditampilkan hanya memiliki ' + str(len(top_customers)) + ' data.'
            print(warning_text)

            labels = []
            data = []
            for customer in top_customers:
                labels.append(customer['pelanggan__nama_pelanggan'])
                data.append(customer['count'])

            # Serialize the data to JSON format
            labels_json = json.dumps(labels)
            data_json = json.dumps(data)

            context = {
                'labels': labels_json,
                'data': data_json,
                'username': request.session['username'],
                'jabatan': request.session['jabatan'],
                'num_top_customers': num_top_customers,
                'warning_text': warning_text,
            }

            return render(request, 'top-customers-chart.html', context)
        else:
            return HttpResponseRedirect ("/")
    else:
        return HttpResponseRedirect("/login")

def sparepart_chart_stock(request):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan':
            spareparts = SparePart.objects.all().order_by('-stok')

            labels = [sparepart.nama for sparepart in spareparts]
            data = [sparepart.stok if sparepart.stok <= 100 else 100 for sparepart in spareparts]

            # Serialize the data to JSON format
            labels_json = json.dumps(labels)
            data_json = json.dumps(data)

            context = {
                'labels': labels_json,
                'data': data_json,
                'username': request.session['username'],
                'jabatan': request.session['jabatan'],
            }

            return render(request, 'sparepart-by-stock.html', context)
        else:
            return HttpResponseRedirect ("/")
    else:
        return HttpResponseRedirect("/login")

def appointment_chart_top_karyawan(request):
    if is_authenticated(request):
        if request.session['jabatan'] !='Inventori' and request.session['jabatan'] !='Teknisi':
            num_top_karyawan = request.GET.get('num_top_karyawan', 5)
            try:
                num_top_karyawan = int(num_top_karyawan)
            except ValueError:
                num_top_karyawan = 5  

            top_karyawan = Appointment.objects \
                .exclude(teknisi=None) \
                .values('teknisi__nama_karyawan') \
                .annotate(count=Count('id')) \
                .order_by('-count')[:num_top_karyawan]

            # Test case
            warning_text= ''
            if (len(top_karyawan) < num_top_karyawan):
                warning_text = 'Data top ' + str(num_top_karyawan) + ' loyalitas customer yang ditampilkan hanya memiliki ' + str(len(top_karyawan)) + ' data.'
            print(warning_text)

            labels = []
            data = []
            for karyawan in top_karyawan:
                labels.append(karyawan['teknisi__nama_karyawan'])
                data.append(karyawan['count'])

            # Serialize the data to JSON format
            labels_json = json.dumps(labels)
            data_json = json.dumps(data)

            context = {
                'labels': labels_json,
                'data': data_json,
                'username': request.session['username'],
                'jabatan': request.session['jabatan'],
                'num_top_karyawan': num_top_karyawan,
                'warning_text': warning_text,
            }

            return render(request, 'top-karyawan-chart.html', context)
        else:
            return HttpResponseRedirect ("/")
    else:
        return HttpResponseRedirect("/login")

def appointment_chart_services(request):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan':
            num_top_services = request.GET.get('num_top_services', 5)
            try:
                num_top_services = int(num_top_services)
            except ValueError:
                num_top_services = 5 

            services = AppointmentService.objects.values('service__nama').annotate(count=Count('service_id')).order_by('-count')[:num_top_services]
            print
            # Test case
            warning_text= ''
            if (len(services) < num_top_services):
                warning_text = 'Data top ' + str(num_top_services) + ' loyalitas customer yang ditampilkan hanya memiliki ' + str(len(services)) + ' data.'
            print(warning_text)

            labels = []
            data = []
            for service in services:
                labels.append(service['service__nama'])
                data.append(service['count'])

            # Serialize the data to JSON format
            labels_json = json.dumps(labels)
            data_json = json.dumps(data)

            context = {
                'labels': labels_json,
                'data': data_json,
                'username': request.session['username'],
                'jabatan': request.session['jabatan'],
                'num_top_services': num_top_services,
                'warning_text': warning_text,
            }

            return render(request, 'top-services-chart.html', context)
        else:
            return HttpResponseRedirect ("/")
    else:
        return HttpResponseRedirect("/login")

def appointment_chart_sparepart(request):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan':
            num_top_services = request.GET.get('num_top_services', 5)
            try:
                num_top_services = int(num_top_services)
            except ValueError:
                num_top_services = 5 

            service_in_appointment = AppointmentService.objects.values_list('service__id', flat=True)
            list_services = []

            for id in service_in_appointment:
                list_services.append(Service.objects.get(id=id))

            list_sparepart = []
            for service in list_services:
                spare_parts = service.kebutuhan_spare_part.all()
                spare_part_names = [spare_part.nama for spare_part in spare_parts]
                list_sparepart.append(spare_part_names)
            
            spareparts = sum(list_sparepart, [])
            spareparts_count = Counter(spareparts)
            spareparts_dict = dict(spareparts_count)

            labels = []
            data = []
            for key, value in spareparts_dict.items():
                labels.append(key)
                data.append(value)

            # Serialize the data to JSON format
            labels_json = json.dumps(labels)
            data_json = json.dumps(data)

            context = {
                'labels': labels_json,
                'data': data_json,
                'username': request.session['username'],
                'jabatan': request.session['jabatan'],
                'num_top_services': num_top_services,
            }

            return render(request, 'top-services-chart.html', context)
        else:
            return HttpResponseRedirect ("/")
    else:
        return HttpResponseRedirect("/login")