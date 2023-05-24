from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .models import SparePart
from services.models import Service
from .forms import SparePartForm, SparepartSearchForm, SparepartSortForm
# from django.core.paginator import Paginator
from django.db import connection

def is_authenticated(request):
    try:
        request.session['username']
        return True
    except:
        return False


def sparepart_list(request):
    if is_authenticated(request):
        if request.session['jabatan'] != 'Akuntan':
            tampung = {}

            # Service from sparepart
            sparepart = SparePart.objects.prefetch_related('services').all()
            for item in sparepart:
                if item.services.all().exists():
                    tampung[item.id] = list(item.services.all())

            # Service langsung
            tampung2 = {}
            cursor = connection.cursor()
            cursor.execute("SET search_path TO public")
            cursor.execute('SELECT * FROM public."services_service_kebutuhan_spare_part"')
            rows = cursor.fetchall()

            for j in range(len(rows)):
                id_service = rows[j][1]
                obj_service = Service.objects.get(id=id_service)
                id_sparepart = rows[j][2]

                if id_sparepart in tampung2:
                    tampung2[id_sparepart] += [obj_service]
                else:
                    tampung2[id_sparepart] = [obj_service]
                    
            for key, value in tampung2.items():
                if key in tampung:
                        tampung[key] += value
                else:
                    tampung[key] = value

            for key in tampung:
                tampung[key] = list(set(tampung[key]))

            form = SparepartSearchForm(request.GET)
            form_sort = SparepartSortForm(request.GET)
            
            if form.is_valid():
                search_query = form.cleaned_data.get('search_query')
                # print(search_query)
                
                if search_query:
                    sparepart = sparepart.filter(nama__icontains=search_query) | sparepart.filter(variasi__icontains=search_query)
            
            if form_sort.is_valid():
                pilihan = form_sort.cleaned_data.get('pilihan')

                if pilihan:
                    if pilihan == 'Terbanyak':
                        sparepart = sparepart.order_by("-stok")
                    elif pilihan == 'Terdikit':
                        sparepart = sparepart.order_by("stok")

            response = {'form':form, 'form_sort': form_sort, 'sparepart': sparepart, 'username': request.session['username'],
                        'jabatan': request.session['jabatan'], 'listallservice': tampung}
            
            return render(request, 'list-spare-part.html', response)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")


def add_sparepart(request):
    if is_authenticated(request):
        if request.session['jabatan'] != 'Akuntan':
            context = {}
            all_services = Service.objects.all()
            all_sparepart = SparePart.objects.all()
            max_id = 0
            
            for sparepart in all_sparepart:
                if sparepart.id > max_id:
                    max_id = sparepart.id
            
            print(max_id)

            form = SparePartForm(request.POST or None)
            if (form.is_valid() and request.method == 'POST'):
                sparepart = form.save(commit=False)
                sparepart.id = max_id + 1  
                sparepart.save() 
                print(sparepart.id)
                return redirect('/list-sparepart')

            context['form'] = form
            context['listservices'] = all_services
            context['username'] = request.session['username']
            context['jabatan'] = request.session['jabatan']
            return render(request, 'create-spare-part.html', context)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")

def ambil_service(id):
    cursor = connection.cursor()
    cursor1 = connection.cursor()
    cursor.execute("SET search_path TO public")
    cursor.execute(
        'SELECT service_id FROM public."services_service_kebutuhan_spare_part" WHERE '
        '"services_service_kebutuhan_spare_part"."sparepart_id"=%s',
        [id])
    rows = cursor.fetchall()

    tampungservice = []
    cursor1.execute("SET search_path TO public")
    for k in range(len(rows)):
        cursor1.execute(
            'SELECT nama FROM public."services_service" WHERE '
            '"services_service"."id"=%s',
            [rows[k][0]])
        rows1 = cursor1.fetchone()
        tampungservice.append(rows1[0])

    return tampungservice


def delete_sparepart(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] != 'Akuntan':
            sparepart = SparePart.objects.get(id=id)
            sparepart.delete()
            spareparts = SparePart.objects.all().values()
            response = {'spareparts': spareparts, 'username': request.session['username'],
                        'jabatan': request.session['jabatan']}
            return redirect('/list-sparepart')
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")


def update_sparepart(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] != 'Akuntan':
            all_services = Service.objects.all()
            obj = SparePart.objects.prefetch_related('services').get(id=id)
            form = SparePartForm(request.POST or None, instance=obj)

            # Kebutuhan spare part table
            service = Service.objects.filter(kebutuhan_spare_part=obj)
            print(service)
            if form.is_valid():
                form.save()
                return redirect('/list-sparepart')
            
            response = {'listservices': all_services,
                        'form': form,
                        'sparepart': obj,
                        'serv':service,
                        'username': request.session['username'],
                        'jabatan': request.session['jabatan']
                        }
            return render(request, "update-spare-part.html", response)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")