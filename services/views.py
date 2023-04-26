from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .models import Service
from .forms import ServiceForm, SparePartItemForm
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
                ids = form.save()
                id_service = ids.id
                return redirect(f"/add-spareparts/{id_service}")

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
            service_by_id = Service.objects.get(id=id)

            context = {}
            context['data'] = service_by_id
            context['username'] = request.session['username']
            context['jabatan'] = request.session['jabatan']
            context['kebutuhan_spare_part'] = service_by_id.kebutuhan_spare_part

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

            nama_spare_part = []
            for h in range(len(spare_part_id)):
                cursor.execute('SELECT nama  FROM public."sparepart_sparepart" WHERE '
                               ' "id"=%s', [spare_part_id[h]])
                rows1 = cursor.fetchall()
                cursor.execute('SELECT variasi  FROM public."sparepart_sparepart" WHERE '
                               ' "id"=%s', [spare_part_id[h]])
                rows2 = cursor.fetchall()
                nama_fix = rows1[0][0] + " " + rows2[0][0]
                nama_spare_part.append(nama_fix)

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
                    response = {'formset': formset, 'nama_spare_part': nama_spare_part, 'username': request.session['username'],
                                'jabatan': request.session['jabatan']}
                    return render(request, "add_kebutuhan_spare_part.html", response)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")