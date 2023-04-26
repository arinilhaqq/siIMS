from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

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
            'appointment': Appointment.objects.get(id=id),
            'username': request.session['username'],
            'jabatan': request.session['jabatan'],
        }
        return render(request, 'create-final-inspection.html', context)
    else:
        return HttpResponseRedirect("/login")
    # if is_authenticated(request):
    #     if request.session['jabatan'] !='Akuntan' and request.session['jabatan'] !='Inventori' and request.session['jabatan'] !='Service Advisor':
    #         if request.method == 'POST':
    #             form = FinalInspectionForm(request.POST)

    #             if form.is_valid():
    #                 form.appointment = Appointment.objects.get(id=id)
    #                 final_inspection = form.save()

    #                 return redirect('/update-final-inspection/' + str(final_inspection.id), final_inspection.id)
    #         else:
    #             form = FinalInspectionForm()

    #         context = {
    #             'form': form,
    #             'appointment': Appointment.objects.get(id=id),
    #             'username': request.session['username'],
    #             'jabatan': request.session['jabatan'],
    #         }
    #         return render(request, 'create-final-inspection.html', context)
    #     else:
    #         return HttpResponseRedirect ("/")
    # else:
    #     return HttpResponseRedirect("/login")
    

def update_final_inspection(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan' and request.session['jabatan'] !='Inventori' and request.session['jabatan'] !='Service Advisor':
            final_inspection = FinalInspection.objects.get(appointment=id)
            print(final_inspection)
            # final_inspection = get_object_or_404(FinalInspection,id=id)
            response = {
            'inspection': final_inspection,
            'username': request.session['username'],
            'jabatan': request.session['jabatan'],
            'appointment': Appointment.objects.get(id=id),
            }
            # context['inspection']=final_inspection
            
            if request.method == "POST":
                form = FinalInspectionForm(request.POST, instance=final_inspection)
                print(form.errors)
                print ('xoxoxoxoxo')
                # response['form'] = form
                if form.is_valid():
                    print (form.cleaned_data)
                    form.save()
                return redirect('/')
            # context['username'] = request.session['username']
            # context['jabatan'] = request.session['jabatan']
            return render(request, "update-final-inspection.html", response)
        else:
            return HttpResponseRedirect ("/")
    else:
        return HttpResponseRedirect("/login")
    
# def update_karyawan(request, id):
#     if is_authenticated(request):
#         if request.session['jabatan'] !='Akuntan' and request.session['jabatan'] !='Inventori'and request.session['jabatan'] !='Teknisi' and request.session['jabatan'] !='Service Advisor':
#             context = {}
#             karyawan = Karyawan.objects.get(id=id)
#             context['karyawan']=karyawan
            
#             form = KaryawanForm(request.POST, instance=karyawan)
#             print(form.is_valid()) # False
#             if (form.is_valid() and request.method == 'POST'):
#                 form.save()
#                 return redirect('/list-karyawan/')
#             context['form'] = form
#             context['username'] = request.session['username']
#             context['jabatan'] = request.session['jabatan']
#             return render(request, 'update-karyawan.html', context)
#         else:
#             return HttpResponseRedirect("/")
#     else:
#         return HttpResponseRedirect("/login")

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
            return redirect('/')
        return render(request, 'verify-final-inspection.html', context)
    else:
        return HttpResponseRedirect("/login")
    # if is_authenticated(request):
    #     if request.session['jabatan'] !='Akuntan' and request.session['jabatan'] !='Inventori':
    #         final_inspection = InitialInspection.objects.get(appointment=id)
    #         response = {'inspection': final_inspection, 'username':request.session['username'], 'jabatan':request.session['jabatan']}
    #         if request.method == 'POST':
    #             form = FinalInspectionForm(request.POST, instance=final_inspection)
    #             if form.is_valid():
    #                 form.save()
    #             return redirect('/verify-final-inspection/' + str(final_inspection.id))
    #         return render(request, "verify_final_inspection.html", response)
    #     else:
    #         return HttpResponseRedirect ("/")
    # else:
    #     return HttpResponseRedirect("/login")
