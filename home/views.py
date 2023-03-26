from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from karyawan.models import Karyawan
from django.contrib.auth import update_session_auth_hash
from django.db import connection

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

