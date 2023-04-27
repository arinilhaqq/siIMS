from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .models import Service
from .forms import ServiceForm, ServiceSearchForm, ServiceSortForm
from django.forms import formset_factory
from django.db import connection


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

            form = ServiceSearchForm(request.GET)
            form_sort =ServiceSortForm(request.GET)

            response = {'services': services, 'username':request.session['username'], 'jabatan':request.session['jabatan']}

            if form.is_valid():
                search_query = form.cleaned_data.get('search_query')
                
                if search_query:
                    services = services.filter(nama__icontains=search_query)
            
            if form_sort.is_valid():
                pilihan = form_sort.cleaned_data.get('pilihan')

                if pilihan:
                    if pilihan == 'Termahal':
                        services = services.order_by("-harga")
                    elif pilihan == 'Termurah':
                        services = services.order_by("harga")

            response = {'form':form, 'services': services, 'username':request.session['username'], 'jabatan':request.session['jabatan']}
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
                form.save()
                return redirect('/list-services')
                # return redirect('/add-spareparts')

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

def add_kebutuhan_spare_parts(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan':
            service = Service.objects.get(id=id)
            id_service = service.id
            cursor = connection.cursor()
            cursor.execute("SET search_path TO public")
            cursor.execute(
                'SELECT * FROM public."services_service_kebutuhan_spare_part" WHERE '
                '"services_service_kebutuhan_spare_part"."service_id"=%s',
                [id_service])
            rows = cursor.fetchall()
            spare_part_id = []
            for j in range(len(rows)):
                spare_part_id.append(rows[j][2])
            if len(rows) > 0:
                SparePartFormSet = formset_factory(SparePartItemForm, extra=len(rows))
                if request.method == 'POST':
                    formset = SparePartFormSet(request.POST)
                    if formset.is_valid():
                        quantities = []
                        for formitem in formset:
                            quantity = formitem.cleaned_data['quantity']
                            quantities.append(quantity)
                        for i in range(len(spare_part_id)):
                            cursor.execute('UPDATE public."services_service_kebutuhan_spare_part" SET '
                                           '"kuantitas"=%s WHERE '
                                           '"service_id"=%s AND "sparepart_id"=%s', [quantities[i], id_service, spare_part_id[i]])
                        return redirect('/list-services')

                else:
                    formset = SparePartFormSet
                    response = {'formset': formset, 'username': request.session['username'],
                                'jabatan': request.session['jabatan']}
                    return render(request, "add_kebutuhan_spare_part.html", response)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")