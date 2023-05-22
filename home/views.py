import calendar
from datetime import timedelta, timezone
import datetime
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from appointment.models import Appointment
from karyawan.models import Karyawan
from sparepart.models import SparePart
from django.contrib.auth import update_session_auth_hash
from django.db import connection
from django.db.models import Count

def is_authenticated(request):
    try:
        request.session['username']
        return True
    except:
        return False

def homepage(request):
    print(is_authenticated)
    if is_authenticated(request):
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
    context= {
        'username': request.session['username'],
        'jabatan': request.session['jabatan'],
    }

    return render(request, 'dashboard.html', context)

def appointment_chart_date(request):
    today = datetime.datetime.today()
    start_date = today - timedelta(days=30)

    appointments = Appointment.objects.filter(date__range=(start_date, today)).values('date').annotate(count=Count('id'))
    print(appointments)

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

def appointment_chart_week(request):
    today = datetime.datetime.today()
    start_date = today - timedelta(days=7)
    end_date = today

    appointments = Appointment.objects.filter(date__range=(start_date, end_date)).\
        extra({'week': "EXTRACT(WEEK FROM date)"}).\
        values('week').annotate(count=Count('id'))
    print(appointments)

    labels = []
    data = []
    for appointment in appointments:
        labels.append(f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
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

def appointment_chart_month(request):
    today = datetime.datetime.today()
    start_date = today - timedelta(days=30)

    appointments = Appointment.objects.filter(date__range=(start_date, today)) \
        .extra({'month': "EXTRACT(month FROM date)", 'year': "EXTRACT(year FROM date)"}) \
        .values('month', 'year') \
        .annotate(count=Count('id'))
    print(appointments)

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

def appointment_chart_top_customers(request):
    num_top_customers = request.GET.get('num_top_customers', 5)
    print(num_top_customers)
    try:
        num_top_customers = int(num_top_customers)
    except ValueError:
        num_top_customers = 5  

    today = datetime.datetime.today()
    start_date = today - timedelta(days=30)

    top_customers = Appointment.objects.filter(date__range=(start_date, today)) \
        .values('pelanggan__nama_pelanggan') \
        .annotate(count=Count('id')) \
        .order_by('-count')[:num_top_customers]

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
    }

    return render(request, 'top-customers-chart.html', context)

def sparepart_chart_stock(request):
    spareparts = SparePart.objects.all().order_by('-stok')

    labels = [sparepart.nama for sparepart in spareparts]
    data = [sparepart.stok for sparepart in spareparts]

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

def appointment_chart_top_karyawan(request):
    num_top_karyawan = request.GET.get('num_top_karyawan', 5)
    try:
        num_top_karyawan = int(num_top_karyawan)
    except ValueError:
        num_top_karyawan = 5  

    top_karyawan = Appointment.objects \
        .values('teknisi__nama_karyawan') \
        .annotate(count=Count('id')) \
        .order_by('-count')[:num_top_karyawan]

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
    }

    return render(request, 'top-karyawan-chart.html', context)