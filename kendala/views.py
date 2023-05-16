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
            
            if request.method == 'POST':
                if form.is_valid():
                    form.save()
                    return redirect('//')
                
            context = {
                'appointment_service': id,
                'username' : request.session['username'],
                'jabatan' : request.session['jabatan'],
                'form' : form,
            }
            return render(request, "create-kendala.html", context)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")