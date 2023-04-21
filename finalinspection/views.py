from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import FinalInspection, Appointment
from .forms import FinalInspectionForm
from django.contrib.auth.decorators import permission_required

def is_authenticated(request):
    try:
        request.session['username']
        return True
    except:
        return False
    
def create_final_inspection(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan' and request.session['jabatan'] !='Inventori' and request.session['jabatan'] !='Service Advisor':
            if request.method == 'POST':
                form = FinalInspectionForm(request.POST)

                if form.is_valid():
                    form.appointment = Appointment.objects.get(id=id)
                    final_inspection = form.save()

                    return redirect('/update-final-inspection/' + str(final_inspection.id), final_inspection.id)
            else:
                form = FinalInspectionForm()

            context = {
                'form': form,
                'appointment': Appointment.objects.get(id=id),
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
            response = {'final_inspection': final_inspection, 'username':request.session['username'], 'jabatan':request.session['jabatan']}

            if request.method == 'POST':
                form = FinalInspectionForm(request.POST, instance=final_inspection)
                if form.is_valid():
                    form.save()
                return redirect('/update-final-inspection/' + str(final_inspection.id), final_inspection.id)
            return render(request, "update_final_inspection.html", response)
        else:
            return HttpResponseRedirect ("/")
    else:
        return HttpResponseRedirect("/login")

def verify_final_inspection(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan' and request.session['jabatan'] !='Inventori':
            final_inspection = FinalInspection.objects.get(appointment=id)
            response = {'final_inspection': final_inspection, 'username':request.session['username'], 'jabatan':request.session['jabatan']}
            if request.method == 'POST':
                form = FinalInspectionForm(request.POST, instance=final_inspection)
                if form.is_valid():
                    form.save()
                return redirect('/verify-final-inspection/' + str(final_inspection.id))
            return render(request, "verify_final_inspection.html", response)
        else:
            return HttpResponseRedirect ("/")
    else:
        return HttpResponseRedirect("/login")
    