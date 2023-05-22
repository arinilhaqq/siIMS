from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from kendala.forms import KendalaForm
from kendala.models import Kendala
from appointment.models import AppointmentService

# Create your views here.

def is_authenticated(request):
    try:
        request.session['username']
        return True
    except:
        return False
    
def create_kendala(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan' and request.session['jabatan'] !='Inventori'and request.session['jabatan'] !='Service Advisor':
            form = KendalaForm(request.POST or None)
            app_service = AppointmentService.objects.get(id=id)
            app_id = app_service.appointment_id
            
            if request.method == 'POST':
                if form.is_valid():
                    form.save()
                    return redirect(f'/service-appointment/{app_id}')
                
            context = {
                'appointment_service': id,
                'status': "Unsolved",
                'username' : request.session['username'],
                'jabatan' : request.session['jabatan'],
                'form' : form,
            }
            return render(request, "create-kendala.html", context)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")

def detail_kendala(request, id):
    if is_authenticated(request):
        kendala = Kendala.objects.get(id=id)

        context = {
            'kendala': kendala,
            'username': request.session['username'],
            'jabatan': request.session['jabatan'],
        }
        return render(request, 'detail-kendala.html', context)
    else:
        return HttpResponseRedirect("/login")

def update_kendala(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan' and request.session['jabatan'] !='Inventori':
            kendala = Kendala.objects.get(id=id)
            appointment_service_id = kendala.appointment_service_id
            appointment_service = AppointmentService.objects.get(id=appointment_service_id)
            appointment_service_id = appointment_service.id

            
            appointment_id = appointment_service.appointment_id
            response = {'kendala': kendala, 'username':request.session['username'], 'jabatan':request.session['jabatan'], 'appointment_service': appointment_service_id}
            form = KendalaForm(request.POST, instance=kendala)
            if (form.is_valid() and request.method == 'POST'):
                form.save()
                return redirect(f'/service-appointment/{appointment_id}')
            # if request.method == 'POST':
            #     form = KendalaForm(request.POST, instance=kendala)
                
            #     if form.is_valid():
            #         form.save()
            #     return redirect(f'service-appointment/{appointment_id}')
                
            return render(request, "update_kendala.html", response)
        else:
            return HttpResponseRedirect ("/")
    else:
        return HttpResponseRedirect("/login")