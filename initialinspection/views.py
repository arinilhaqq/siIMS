from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import InitialInspection, Appointment
from .forms import InitialInspectionForm

def is_authenticated(request):
    try:
        request.session['username']
        return True
    except:
        return False
    
def create_initial_inspection(request, id):
    if is_authenticated(request):
        if request.method == 'POST':
            form = InitialInspectionForm(request.POST)

            if form.is_valid():
                form.appointment = Appointment.objects.get(id=id)
                initial_inspection = form.save()

                return redirect('/detail-initial-inspection/' + str(initial_inspection.id), initial_inspection.id)
        else:
            form = InitialInspectionForm()

        context = {
            'form': form,
            'appointment': Appointment.objects.get(id=id),
            'username': request.session['username'],
            'jabatan': request.session['jabatan'],
        }
        return render(request, 'create-initial-inspection.html', context)
    else:
        return HttpResponseRedirect("/login")

def detail_initial_inspection(request, id):
    if is_authenticated(request):
        initial_inspection = InitialInspection.objects.get(appointment=id)

        context = {
            'inspection': initial_inspection,
            'username': request.session['username'],
            'jabatan': request.session['jabatan'],
            'appointment': Appointment.objects.get(id=id)
        }
        return render(request, 'detail-initial-inspection.html', context)
    else:
        return HttpResponseRedirect("/login")

def update_initial_inspection(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan' and request.session['jabatan'] !='Inventori' and request.session['jabatan'] !='Service Advisor':
            initial_inspection = InitialInspection.objects.get(appointment=id)
            appointment = Appointment.objects.get(id=id)
            response = {
            'inspection': initial_inspection,
            'username': request.session['username'],
            'jabatan': request.session['jabatan'],
            'appointment': appointment,
            }
            
            if request.method == "POST":
                form = InitialInspectionForm(request.POST, instance=initial_inspection)      
                if form.is_valid():
                    print (form.cleaned_data)
                    form.save()
                return redirect('/detail-initial-inspection/' + str(appointment.id), appointment.id)

            return render(request, "update-initial-inspection.html", response)
        else:
            return HttpResponseRedirect ('/detail-initial-inspection/' + str(appointment.id), appointment.id)
    else:
        return HttpResponseRedirect("/login")

