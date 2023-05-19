from django.http import HttpResponseRedirect
from django.shortcuts import render
from appointment.models import Appointment
from .models import NotaBarang, NotaGabungan, NotaJasa
from datetime import date
from django.db import connection
from num2words import num2words

def is_authenticated(request):
    try:
        request.session['username']
        return True
    except:
        return False
    
# def add_nota(request):
#   if is_authenticated(request):
#     if request.session['jabatan'] == 'Akuntan' or request.session['jabatan'] == 'Admin':
#         appointments = Appointment.objects.filter(status='Finished')
          
#         for obj in appointments:
#             nota_barang = NotaBarang()
#             nota_barang.nomor_barang = int(str(obj.id) + "01")
#             serpis = []
#             sperpart = []
#             kuantitas = []
#             total_barang = 0
            
#             for i in obj.services:
#                 serpis.append(i)
#                 for c in i.kebutuhan_spare_part:
#                     sperpart.append(c)

#             cursor = connection.cursor()
#             cursor.execute("SET search_path TO public")           
#             for i in range(len(serpis)):
#                 cursor.execute(
#                     'SELECT * FROM public."services_service_kebutuhan_spare_part" WHERE '
#                     '"services_service_kebutuhan_spare_part"."service_id"=%s',
#                     [serpis[i]])
#                 rows = cursor.fetchall()
#                 for j in range(len(rows)):
#                     kuantitas.append(rows[j][3])

#             for k in range (len(sperpart)):
#                 total_barang += (sperpart[k].harga * kuantitas[k])        
                
#             nota_barang.total_harga_sparepart = total_barang
#             nota_barang.petugas_gudang = False
#             nota_barang.petugas_bengkel = False
#             nota_barang.save()
              
#             nota_jasa = NotaJasa()
#             nota_jasa.nomor_jasa = int(str(obj.id) + "02")
#             total_jasa = 0
#             for servis in obj.services:
#                 total_jasa += servis.harga
#             nota_jasa.total_harga_jasa = total_jasa
#             nota_jasa.save()
              
#             nota_gabungan= NotaGabungan()
#             nota_gabungan.tanggal = date.today()
#             nota_gabungan.appointment = obj
#             nota_gabungan.nota_barang = nota_barang
#             nota_gabungan.nota_jasa = nota_jasa
#             nota_gabungan.nomor_gabungan = int(str(obj.id) + "03")
#             nota_gabungan.total_harga_gabungan = total_jasa + total_barang
#             nota_gabungan.save()

#             response = {
#                 'appointment': appointments,
#                 'username': request.session['username'],
#                 'jabatan': request.session['jabatan']
#             }

#             return render(request, 'list-nota.html', response)
#         else:
#             return HttpResponseRedirect("/")
#     else:
#         return HttpResponseRedirect("/login")

def add_nota(id):
    appointment = Appointment.objects.get(id=id)
    if (appointment.status=='Finished'):
        nota_barang = NotaBarang()
        nota_barang.nomor_barang = int(str(id) + "01")
        serpis = []
        sperpart = []
        kuantitas = []
        total_barang = 0
        for i in appointment.services.all():
            serpis.append(i)
            for c in i.kebutuhan_spare_part.all():
                sperpart.append(c)

        cursor = connection.cursor()
        cursor.execute("SET search_path TO public")           
        for i in range(len(serpis)):
            cursor.execute('SELECT * FROM public."services_service_kebutuhan_spare_part" WHERE '
                    '"services_service_kebutuhan_spare_part"."service_id"=%s',
                    [serpis[i].id])
            rows = cursor.fetchall()
            for j in range(len(rows)):
                kuantitas.append(rows[j][3])

        for k in range (len(sperpart)):
            total_barang += (sperpart[k].harga * kuantitas[k])        
                
        nota_barang.total_harga_sparepart = total_barang
        nota_barang.petugas_gudang = False
        nota_barang.petugas_bengkel = False
        nota_barang.save()
              
        nota_jasa = NotaJasa()
        nota_jasa.nomor_jasa = int(str(appointment.id) + "02")
        total_jasa = 0
        for servis in appointment.services.all():
            total_jasa += servis.harga
        nota_jasa.total_harga_service = total_jasa
        nota_jasa.save()
              
        nota_gabungan= NotaGabungan()
        nota_gabungan.tanggal = date.today()
        nota_gabungan.appointment = appointment
        nota_gabungan.nota_barang = nota_barang
        nota_gabungan.total_harga_service = total_jasa
        nota_gabungan.total_harga_sparepart = total_barang
        nota_gabungan.nota_jasa = nota_jasa
        nota_gabungan.nomor_gabungan = int(str(appointment.id) + "03")
        nota_gabungan.total_harga_gabungan = total_jasa + total_barang
        nota_gabungan.save()


def nota_list(request):
    if is_authenticated(request):
        if request.session['jabatan'] == 'Akuntan' or request.session['jabatan'] == 'Admin':
            # add_nota(request)
            cursor = connection.cursor()
            cursor.execute("SET search_path TO public")  
            appointment = Appointment.objects.filter(status='Finished').prefetch_related('pelanggan')
            for app in appointment:
                cursor.execute('SELECT * FROM public."nota_notagabungan" WHERE '
                    '"nota_notagabungan"."nomor_gabungan"=%s',
                    [int(str(app.id) + "03")])
                result = cursor.fetchone()
                if not result:
                    add_nota(app.id)

            # form = ServiceSearchForm(request.GET)
            # form_sort = ServiceSortForm(request.GET)

            # response = {'appointment': appointment, 'username': request.session['username'],
            #             'jabatan': request.session['jabatan']}

            # if form.is_valid():
            #     search_query = form.cleaned_data.get('search_query')
            #
            #     if search_query:
            #         services = services.filter(nama__icontains=search_query)
            #
            # if form_sort.is_valid():
            #     pilihan = form_sort.cleaned_data.get('pilihan')
            #
            #     if pilihan:
            #         if pilihan == 'Termahal':
            #             services = services.order_by("-harga")
            #         elif pilihan == 'Termurah':
            #             services = services.order_by("harga")

            response = {
                # 'form': form,
                # 'form_sort': form_sort,
                'appointment': appointment,
                'username': request.session['username'],
                'jabatan': request.session['jabatan']
            }

            return render(request, 'list-nota.html', response)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")


def receipt_view(request, id):
    nota_gabungan = NotaGabungan.objects.get(id=id)
    nota_jasa = nota_gabungan.nota_jasa
    appointment = nota_gabungan.appointment
    pelanggan = appointment.pelanggan.nama_pelanggan
    nomor_pkb = appointment.pelanggan.nomor_pkb
    nomor_polisi = appointment.pelanggan.nomor_polisi
    tanggal = nota_gabungan.tanggal
    serpis = []
    for i in appointment.services.all():
        serpis.append(i)


    context = {
        'nota_jasa': nota_jasa,
        'pelanggan' : pelanggan,
        'nomor_pkb' : nomor_pkb,
        'nomor_polisi' : nomor_polisi,
        'tanggal' : tanggal,
        'appointment':appointment,
        'services': serpis
    }

    return render(request, 'notajasa.html', context)

def barang_view(request, id):
    nota_gabungan = NotaGabungan.objects.get(id=id)
    nota_barang = nota_gabungan.nota_barang
    appointment = nota_gabungan.appointment
    pelanggan = appointment.pelanggan.nama_pelanggan
    nomor_pkb = appointment.pelanggan.nomor_pkb
    nomor_polisi = appointment.pelanggan.nomor_polisi
    tanggal = nota_gabungan.tanggal

    tampung1 = {} #kuantitas
    tampung2 = {} #harga total per sparepart
    tampung3 = {} #harga satuan
    

    serpis = []
    sperpart = []
    kuantitas = []
    harga_total_peritem = []
            
    for i in appointment.services.all():
        serpis.append(i)
        for c in i.kebutuhan_spare_part.all():
            sperpart.append(c)
            tampung3[c.nama] = c.harga 
            
            # tampung1.append(c.nama)
            # tampung2.append(c.nama)

    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")           
    for i in range(len(serpis)):
        cursor.execute(
            'SELECT * FROM public."services_service_kebutuhan_spare_part" WHERE '
            '"services_service_kebutuhan_spare_part"."service_id"=%s',
            [serpis[i].id])
        rows = cursor.fetchall()
        for j in range(len(rows)):
            if sperpart[j].nama in tampung1:
                angka = rows[j][3] + tampung1[sperpart[j].nama]
                kuantitas.append(angka)
                tampung1[sperpart[j].nama] = angka
            else:
                kuantitas.append(rows[j][3])
                tampung1[sperpart[j].nama] = rows[j][3] #buat kuantitas

    for k in range(len(sperpart)):
        if sperpart[k].nama in tampung2:
            total = tampung2[sperpart[k].nama]
            total += sperpart[k].harga * kuantitas[k]
            harga_total_peritem.append(total)
        else:
            tampung2[sperpart[k].nama] = sperpart[k].harga * kuantitas[k]
            harga_total_peritem.append(sperpart[k].harga * kuantitas[k])

    print(kuantitas)
    print(sperpart[k].harga) 
    print(tampung1)
    print(tampung2)                   

    context = {
        'nota_barang': nota_barang,
        'pelanggan' : pelanggan,
        'nomor_pkb' : nomor_pkb,
        'nomor_polisi' : nomor_polisi,
        'tanggal' : tanggal,
        'sperpart': sperpart,
        'kuantitas': kuantitas,
        'tampung1' : tampung1,
        'tampung2' : tampung2
        # 'harga_total_peritem': harga_total_peritem
    }

    return render(request, 'notabarang.html', context)

def gabungan_view(request, id):
    nota_gabungan = NotaGabungan.objects.get(id=id)
    nota_jasa = nota_gabungan.nota_jasa
    nota_barang = nota_gabungan.nota_barang
    appointment = nota_gabungan.appointment
    pelanggan = appointment.pelanggan.nama_pelanggan
    nomor_pkb = appointment.pelanggan.nomor_pkb
    nomor_polisi = appointment.pelanggan.nomor_polisi
    tanggal = nota_gabungan.tanggal
    total_harga_gabungan = nota_gabungan.total_harga_gabungan
    total_harga_sparepart = nota_gabungan.total_harga_sparepart
    total_harga_service = nota_gabungan.total_harga_service
    total_harga_lainlain = nota_gabungan.total_harga_lainlain
    keterangan_lain_lain = nota_gabungan.keterangan_lain_lain
    jenis = appointment.pelanggan.jenis_mobil

    
    
    # print(appointment.services.kebutuhan_spare_part)

    # Nomor_nota_jasa= "XXXXYYYY"
    # Nomor_nota_barang= "XXXXYYYY"
    # keterangan_lain_lain = "LalalaUwuwuw"
    # total_harga_sparepart = 20000
    # total_harga_service = 20000
    # total_harga_lainlain = 40000

    # total_harga_gabungan = 10000

    harga_terbilang = num2words(total_harga_gabungan, lang='id')


    context = {
        'Nomor_nota_jasa': nota_jasa.nomor_jasa,
        'Nomor_nota_barang': nota_barang.nomor_barang,
        'keterangan_lain_lain' : keterangan_lain_lain,
        'total_harga_sparepart' : total_harga_sparepart,
        'total_harga_service' : total_harga_service,
        'total_harga_lainlain' : total_harga_lainlain,
        'nomor_gabungan': nota_gabungan.nomor_gabungan,
        # 'nota_jasa': nota_jasa,
        # 'nota_barang': nota_barang,

        'total_harga_gabungan' : total_harga_gabungan,

        'harga_terbilang' : harga_terbilang,
        'pelanggan' : pelanggan,
        'nomor_pkb' : nomor_pkb,
        'nomor_polisi' : nomor_polisi,
        'tanggal' : tanggal,
        'jenis': jenis
    }

    return render(request, 'notagabungan.html', context)
