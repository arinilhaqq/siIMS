from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .models import Service
from .forms import ServiceForm

def is_authenticated(request):
    try:
        request.session['username']
        return True
    except:
        return False
    
def services_list(request):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan':
            services = Service.objects.all().values()  
            response = {'services': services, 'username':request.session['username'], 'jabatan':request.session['jabatan']}
            return render(request, 'list-services.html', response)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")

def add_service(request):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan':
            context = {}

            form = ServiceForm(request.POST or None)
            if (form.is_valid() and request.method == 'POST'):
                # kebutuhan_spare_part = form.cleaned_data['kebutuhan_spare_part']
                # kuantitas_spare_part = form.cleaned_data['kuantitas_spare_part']
                form.save()
                return redirect('/list-services')

            context['form'] = form
            context['username'] = request.session['username']
            context['jabatan'] = request.session['jabatan']
            return render(request, 'create-services.html', context)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")


def detail_service(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan':
            context = {}
            context["data"] = Service.objects.get(id=id)
            context['username'] = request.session['username']
            context['jabatan'] = request.session['jabatan']
            return render(request, "list-services.html", context)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")

def delete_service(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan':
            service = Service.objects.get(id=id)
            service.delete()
            services = Service.objects.all().values()
            response = {'services': services, 'username':request.session['username'], 'jabatan':request.session['jabatan']}
            return render(request, 'list-services.html', response)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")


def update_service(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan':
            obj = get_object_or_404(Service, id=id)
            form = ServiceForm(request.POST or None, instance=obj)
            if form.is_valid():
                form.save()
                return redirect('/list-services')
            response = {'form': form, 'service': obj, 'username':request.session['username'], 'jabatan':request.session['jabatan']}
            return render(request, "update-services.html", response)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")