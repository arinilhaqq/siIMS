from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .models import Service
from sparepart.models import SparePart
from .forms import ServiceForm, SparePartItemForm, ServiceSearchForm, ServiceSortForm
from django.forms import formset_factory
from django.db import connection


def is_authenticated(request):
    try:
        request.session['username']
        return True
    except:
        return False
    
def services_list(request):
    SATUAN_WAKTU = (('Menit', 'Menit'),
                    ('Jam', 'Jam'),
                    ('Hari', 'Hari'),
                    ('Minggu', 'Minggu'),
                    ('Bulan', 'Bulan'))

    if is_authenticated(request):
        if request.session['jabatan'] != 'Akuntan':
            tampung = {}

            # Sparepart from service
            services = Service.objects.prefetch_related('kebutuhan_spare_part').all()
            for item in services:
                if item.kebutuhan_spare_part.all().exists():
                    tampung[item.id] = list(item.kebutuhan_spare_part.all())

            # Sparepart langsung
            tampung2 = {}
            cursor = connection.cursor()
            cursor.execute("SET search_path TO public")
            cursor.execute('SELECT * FROM public."sparepart_sparepart_services"')
            rows = cursor.fetchall()

            for j in range(len(rows)):
                id_sparepart = rows[j][1]
                obj_sparepart = SparePart.objects.get(id=id_sparepart)
                id_service = rows[j][2]

                if id_service in tampung2:
                    tampung2[id_service] += [obj_sparepart]
                else:
                    tampung2[id_service] = [obj_sparepart]
                    
            for key, value in tampung2.items():
                if key in tampung:
                        tampung[key] += value
                else:
                    tampung[key] = value

            for key in tampung:
                tampung[key] = list(set(tampung[key]))

            # print(tampung)
            form = ServiceSearchForm(request.GET)
            form_sort =ServiceSortForm(request.GET)

            if form.is_valid():
                search_query = form.cleaned_data.get('search_query')
                
                if search_query:
                    services = services.filter(nama__icontains=search_query)
            
            if form_sort.is_valid():
                pilihan = form_sort.cleaned_data.get('pilihan')

                if pilihan:
                    if pilihan == 'Terlama':
                        services = services.order_by("jumlah_estimasi_pengerjaan", "satuan_waktu")
                    elif pilihan == 'Tercepat':
                        services = services.order_by("-jumlah_estimasi_pengerjaan", "-satuan_waktu")
                    elif pilihan == 'Termahal':
                        services = services.order_by("-harga")
                    elif pilihan == 'Termurah':
                        services = services.order_by("harga")

            response = {
                'form':form,
                'form_sort': form_sort,
                'services': services,
                'username':request.session['username'],
                'jabatan':request.session['jabatan'],
                'listallspareparts': tampung
            }
            
            return render(request, 'list-services.html', response)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")

def ambil_sparepart(id):
    cursor = connection.cursor()
    cursor1 = connection.cursor()
    cursor.execute("SET search_path TO public")
    cursor.execute(
        'SELECT sparepart_id FROM public."sparepart_sparepart_services" WHERE '
        '"sparepart_sparepart_services"."service_id"=%s',
        [id])
    rows = cursor.fetchall()

    tampungsparepart = []
    cursor1.execute("SET search_path TO public")
    for k in range(len(rows)):
        cursor1.execute(
            'SELECT nama, variasi FROM public."sparepart_sparepart" WHERE '
            '"sparepart_sparepart"."id"=%s',
            [rows[k][0]])
        rows1 = cursor1.fetchone()
        tampungsparepart.append(rows1[0])

    return tampungsparepart

def add_service(request):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan' and request.session['jabatan'] !='Owner':
            context = {}
            all_sparepart = SparePart.objects.all()

            form = ServiceForm(request.POST or None)
            if (form.is_valid() and request.method == 'POST'):

                ids = form.save()
                id_service = ids.id
                return redirect(f"/add-spareparts/{id_service}")

            context['form'] = form
            context['listsparepart'] = all_sparepart
            context['username'] = request.session['username']
            context['jabatan'] = request.session['jabatan']

            return render(request, 'create-services.html', context)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")


def delete_service(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan' and request.session['jabatan'] !='Owner':
            service = Service.objects.get(id=id)
            service.delete()
            services = Service.objects.all().values()

            response = {
                'services': services,
                'username':request.session['username'],
                'jabatan':request.session['jabatan']
            }

            return redirect('/list-services')
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")


def update_service(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan' and request.session['jabatan'] !='Owner':
            all_sparepart = SparePart.objects.all()
            obj = Service.objects.prefetch_related('kebutuhan_spare_part').get(id=id)

            # Sparepart services table
            sparepart = SparePart.objects.filter(services=obj)

            form = ServiceForm(request.POST or None, instance=obj)

            if form.is_valid():
                ids = form.save()
                id_service = ids.id
                return redirect(f"/add-spareparts/{id_service}")

            response = {
                'form': form,
                'listsparepart': all_sparepart,
                'service': obj,
                'spares': sparepart,
                'username':request.session['username'],
                'jabatan':request.session['jabatan']
            }

            return render(request, "update-services.html", response)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")


def add_kebutuhan_spare_parts(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan' and request.session['jabatan'] !='Owner':
            service = Service.objects.get(id=id)
            id_service = service.id
            cursor = connection.cursor()
            cursor1 = connection.cursor()
            cursor.execute("SET search_path TO public")
            cursor.execute(
                'SELECT * FROM public."services_service_kebutuhan_spare_part" WHERE '
                '"services_service_kebutuhan_spare_part"."service_id"=%s',
                [id_service])
            rows = cursor.fetchall()
            spare_part_id = []
            sparepart_id_kuantitas = {}
            
            for j in range(len(rows)):
                spare_part_id.append(rows[j][2])
                sparepart_id_kuantitas[rows[j][2]] = rows[j][3]

            # print(len(rows))
            # print(rows)

            tampung = []
            for s in range(len(rows)): #ambil semua hasil final
                cursor1.execute("SET search_path TO public")
                cursor1.execute(
                    'SELECT nama, variasi FROM public."sparepart_sparepart" WHERE '
                    '"sparepart_sparepart"."id"=%s',
                    [rows[s][2]])
                rows1 = cursor1.fetchone()
                print(rows1)
                tampung.append(rows1[0])

            not_in_subset = [item for item in ambil_sparepart(id) if item not in tampung]
            cursor2 = connection.cursor()
            cursor2.execute("SET search_path TO public")
            cursor2.execute(
                'DELETE FROM public."sparepart_sparepart_services" WHERE '
                '"sparepart_id" IN (SELECT id FROM public."sparepart_sparepart" WHERE nama = ANY (%s::text[]))',
                (not_in_subset,)
            )

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
                    response = {'sparepart_id_kuantitas': sparepart_id_kuantitas, 'formset': formset, 'nama_spare_part': nama_spare_part, 'username': request.session['username'],
                                'jabatan': request.session['jabatan']}
                    return render(request, "add_kebutuhan_spare_part.html", response)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")