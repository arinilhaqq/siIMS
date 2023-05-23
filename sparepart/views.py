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
            sparepart = SparePart.objects.prefetch_related('services').all()

            tampung = {}

            for item in sparepart:
                tampung[item.id] = ambil_service(item.id)

            form = SparepartSearchForm(request.GET)
            form_sort = SparepartSortForm(request.GET)
            

            if form.is_valid():
                search_query = form.cleaned_data.get('search_query')
                print(search_query)
                
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
                        'jabatan': request.session['jabatan'], 'serpis': tampung}
            
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

            form = SparePartForm(request.POST or None)
            if (form.is_valid() and request.method == 'POST'):
                form.save()
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

            # cursor = connection.cursor()
            # cursor.execute("SET search_path TO public")
            # cursor.execute(
            #     'SELECT service_id FROM public."services_service_kebutuhan_spare_part" WHERE '
            #     '"services_service_kebutuhan_spare_part"."sparepart_id"=%s',
            #     [id])
            # rows = cursor.fetchall()
            # tampungserv = []
            #
            # for i in range(len(rows)):
            #     serv = Service.objects.get(id=rows[i][0])
            #     tampungserv.append(serv)

            # 'tampungserv': tampungserv

            obj = get_object_or_404(SparePart, id=id)
            form = SparePartForm(request.POST or None, instance=obj)
            if form.is_valid():
                form.save()
                return redirect('/list-sparepart')
            response = {'listservices': all_services, 'form': form, 'sparepart': obj, 'username': request.session['username'],
                        'jabatan': request.session['jabatan']}
            return render(request, "update-spare-part.html", response)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")