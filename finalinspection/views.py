from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from initialinspection.models import InitialInspection

from .models import FinalInspection, Appointment
from .forms import FinalInspectionForm

def is_authenticated(request):
    try:
        request.session['username']
        return True
    except:
        return False
    
def create_final_inspection(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan' and request.session['jabatan'] !='Inventori' and request.session['jabatan'] !='Service Advisor':
            appointment = Appointment.objects.get(id=id)
            initial_inspection=InitialInspection.objects.get(appointment=id)
            if request.method == 'POST':
                form = FinalInspectionForm(request.POST)

                if form.is_valid():
                    form.appointment = Appointment.objects.get(id=id)
                    final_inspection = form.save()

                    return redirect('/verify-final-inspection/' + str(id), id)
            else:
                form = FinalInspectionForm()

            context = {
                'form': form,
                'intial_inspection': initial_inspection,
                'appointment': appointment,
                'username': request.session['username'],
                'jabatan': request.session['jabatan'],
            }
            return render(request, 'create-final-inspection.html', context)
        else:
            return HttpResponseRedirect ("/")
    else:
        return HttpResponseRedirect("/login")
    
def update_final_inspection(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan' and request.session['jabatan'] !='Inventori' and request.session['jabatan'] !='Service Advisor':
            final_inspection = FinalInspection.objects.get(appointment=id)
            print(final_inspection)
            response = {
            'inspection': final_inspection,
            'username': request.session['username'],
            'jabatan': request.session['jabatan'],
            'appointment': Appointment.objects.get(id=id),
            }
            
            if request.method == "POST":
                form = FinalInspectionForm(request.POST, instance=final_inspection)
                print(form.errors)
                if form.is_valid():
                    print (form.cleaned_data)
                    form.save()
                return redirect('/verify-final-inspection/' + str(id), id)
            return render(request, "update-final-inspection.html", response)
        else:
            return HttpResponseRedirect ("/")
    else:
        return HttpResponseRedirect("/login")
    
def verify_final_inspection(request, id):
    if is_authenticated(request):
        final_inspection = FinalInspection.objects.get(appointment=id)

        context = {
            'inspection': final_inspection,
            'username': request.session['username'],
            'jabatan': request.session['jabatan'],
            'appointment': Appointment.objects.get(id=id),
        }
        if request.method == 'POST':
            form = FinalInspectionForm(request.POST, instance=final_inspection)
            context['form']=form
            print(form.errors)
            if form.is_valid():
                print(form.cleaned_data)
                form.save()
            return redirect('/list-appointment')
        return render(request, 'verify-final-inspection.html', context)
    else:
        return HttpResponseRedirect("/login")
    
