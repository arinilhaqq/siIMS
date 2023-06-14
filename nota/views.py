from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from appointment.models import Appointment
from nota.forms import NotaBarangForms, NotaGabunganForms, NotaSearchForm, NotaSortForm
from .models import NotaBarang, NotaGabungan, NotaJasa
from datetime import date
from django.db import connection
# from num2words import num2words

def is_authenticated(request):
    try:
        request.session['username']
        return True
    except:
        return False
    

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
        if request.session['jabatan'] == 'Akuntan' or request.session['jabatan'] == 'Admin' or request.session['jabatan'] == 'Service Advisor' or request.session['jabatan'] == 'Inventori' or request.session['jabatan'] == 'Teknisi' or request.session['jabatan'] == 'Owner':
            cursor = connection.cursor()
            cursor.execute("SET search_path TO public")  
            id_nota = 0
            id_appointment_nota= {}
            appointment = Appointment.objects.filter(status='Finished').prefetch_related('pelanggan')
            for app in appointment:
                cursor.execute('SELECT * FROM public."nota_notagabungan" WHERE '
                    '"nota_notagabungan"."nomor_gabungan"=%s',
                    [int(str(app.id) + "03")])
                result = cursor.fetchone()
                
                if not result:
                    add_nota(app.id)
                cursor.execute('SELECT id FROM public."nota_notagabungan" WHERE '
                        '"nota_notagabungan"."appointment_id"=%s',
                        [app.id])
                id_nota = cursor.fetchone()[0]
                id_appointment_nota[app.id] = id_nota
                
            form = NotaSearchForm(request.GET)
            form_sort = NotaSortForm(request.GET)


            if form.is_valid():
                search_query = form.cleaned_data.get('search_query')
                
                if search_query:
                    appointment = appointment.filter(pelanggan__nama_pelanggan__icontains=search_query)

            if form_sort.is_valid():
                pilihan = form_sort.cleaned_data.get('pilihan')

                if pilihan:
                    if pilihan == 'Terbaru':
                        appointment = appointment.order_by("-id")
                    elif pilihan == 'Terlama':
                        appointment = appointment.order_by("id")

            response = {
                'form': form,
                'form_sort': form_sort,
                'appointment': appointment,
                'username': request.session['username'],
                'jabatan': request.session['jabatan'],
                'id_nota': id_nota,
                'id_appointment_nota': id_appointment_nota,
            }

            return render(request, 'list-nota.html', response)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")


def receipt_view(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] == 'Akuntan' or request.session['jabatan'] == 'Admin' or request.session['jabatan'] == 'Service Advisor' or request.session['jabatan'] == 'Owner':
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
                'username': request.session['username'],
                'jabatan': request.session['jabatan'],
                'services': serpis
            }

            return render(request, 'notajasa.html', context)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")
    
def barang_view(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] == 'Akuntan' or request.session['jabatan'] == 'Admin' or request.session['jabatan'] == 'Inventori' or request.session['jabatan'] == 'Teknisi' or request.session['jabatan'] == 'Service Advisor' or request.session['jabatan'] == 'Owner':
            nota_gabungan = NotaGabungan.objects.get(id=id)
            nota_barang = nota_gabungan.nota_barang
            appointment = nota_gabungan.appointment
            pelanggan = appointment.pelanggan.nama_pelanggan
            nomor_pkb = appointment.pelanggan.nomor_pkb
            nomor_polisi = appointment.pelanggan.nomor_polisi
            tanggal = nota_gabungan.tanggal
            id_oper = id

            tampung1 = {} #kuantitas
            tampung2 = {} #harga total per sparepart
            tampung3 = {} #harga satuan
            

            serpis = []
            sperpart = []
            harga_total_peritem = []
                    
            for i in appointment.services.all():
                serpis.append(i)
                for c in i.kebutuhan_spare_part.all():
                    if c not in sperpart:
                        sperpart.append(c)
                    tampung3[c.nama] = c.harga 

            cursor = connection.cursor()
            cursor.execute("SET search_path TO public")           
            for i in range(len(serpis)):
                cursor.execute(
                    'SELECT * FROM public."services_service_kebutuhan_spare_part" WHERE '
                    '"services_service_kebutuhan_spare_part"."service_id"=%s',
                    [serpis[i].id])
                rows = cursor.fetchall()
                print(len(rows))
                for j in range(len(rows)):
                    if sperpart[j].nama in tampung1.keys():
                        angka = rows[j][3] + tampung1[sperpart[j].nama]
                        tampung1[sperpart[j].nama] = angka
                    else:
                        tampung1[sperpart[j].nama] = rows[j][3] #buat kuantitas
                        
            for k in range(len(sperpart)):
                print("Sperpart: ", sperpart)
                if sperpart[k].nama in tampung2:
                    total = tampung2[sperpart[k].nama]
                    total += sperpart[k].harga * tampung1[sperpart[k].nama]
                    harga_total_peritem.append(total)
                else:
                    print("Hello its tampung")
                    print(sperpart[k].nama)
                    tampung2[sperpart[k].nama] = sperpart[k].harga * tampung1[sperpart[k].nama]
                    harga_total_peritem.append(sperpart[k].harga * tampung1[sperpart[k].nama])                 

            context = {
                'nota_barang': nota_barang,
                'pelanggan' : pelanggan,
                'nomor_pkb' : nomor_pkb,
                'nomor_polisi' : nomor_polisi,
                'tanggal' : tanggal,
                'sperpart': sperpart,
                'serpis': serpis,
                'username': request.session['username'],
                'jabatan': request.session['jabatan'],
                'tampung1' : tampung1,
                'tampung2' : tampung2,
                'tampung3' : tampung3,
                'id_oper': id_oper
            }

            return render(request, 'notabarang.html', context)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")



def gabungan_view(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] == 'Akuntan' or request.session['jabatan'] == 'Admin' or request.session['jabatan'] == 'Service Advisor' or request.session['jabatan'] == 'Inventori' or request.session['jabatan'] == 'Teknisi' or request.session['jabatan'] == 'Owner':
            nota_gabungan = NotaGabungan.objects.get(id=id)
            id_oper = id
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


            # harga_terbilang = num2words(total_harga_gabungan, lang='id')


            context = {
                'Nomor_nota_jasa': nota_jasa.nomor_jasa,
                'Nomor_nota_barang': nota_barang.nomor_barang,
                'keterangan_lain_lain' : keterangan_lain_lain,
                'total_harga_sparepart' : total_harga_sparepart,
                'total_harga_service' : total_harga_service,
                'total_harga_lainlain' : total_harga_lainlain,
                'nomor_gabungan': nota_gabungan.nomor_gabungan,
                'username': request.session['username'],
                'jabatan': request.session['jabatan'],
                'total_harga_gabungan' : total_harga_gabungan,
                # 'harga_terbilang' : harga_terbilang,
                'pelanggan' : pelanggan,
                'nomor_pkb' : nomor_pkb,
                'nomor_polisi' : nomor_polisi,
                'tanggal' : tanggal,
                'jenis': jenis,
                'id_oper': id_oper
            }

            return render(request, 'notagabungan.html', context)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")

def update_notagabungan(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] =='Akuntan' or request.session['jabatan'] == 'Admin' or request.session['jabatan'] == 'Teknisi' or request.session['jabatan'] == 'Inventori':
            nota_gabungan = NotaGabungan.objects.get(id=id)
            appointment = nota_gabungan.appointment
            nomor_pkb = appointment.pelanggan.nomor_pkb
            nomor_polisi = appointment.pelanggan.nomor_polisi
            pelanggan = appointment.pelanggan.nama_pelanggan
            jenis = appointment.pelanggan.jenis_mobil

            form = NotaGabunganForms(request.POST or None, instance=nota_gabungan)

            if form.is_valid():
                form.save()
                nota_gabungan.total_harga_gabungan= nota_gabungan.total_harga_lainlain + nota_gabungan.total_harga_sparepart + nota_gabungan.total_harga_service
                nota_gabungan.save()
                return redirect("/nota/")

            response = {
                'form': form,
                'nota_gabungan': nota_gabungan,
                'username':request.session['username'],               
                'jabatan':request.session['jabatan'],
                'nomor_pkb': nomor_pkb,
                'username': request.session['username'],
                'jabatan': request.session['jabatan'],
                'nomor_polisi': nomor_polisi,
                'pelanggan': pelanggan,
                'jenis': jenis

            }

            return render(request, "update-notagabungan.html", response)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")


def ceklis_notabarang(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] =='Akuntan' or request.session['jabatan'] == 'Admin' or request.session['jabatan'] == 'Teknisi' or request.session['jabatan'] == 'Inventori':
            nota_gabungan = NotaGabungan.objects.get(id=id)
            nota_barang = nota_gabungan.nota_barang
            form = NotaBarangForms(request.POST or None, instance=nota_barang)
            appointment = nota_gabungan.appointment
            pelanggan = appointment.pelanggan.nama_pelanggan
            nomor_pkb = appointment.pelanggan.nomor_pkb
            nomor_polisi = appointment.pelanggan.nomor_polisi
            tanggal = nota_gabungan.tanggal
            id_oper = id

            tampung1 = {} #kuantitas
            tampung2 = {} #harga total per sparepart
            tampung3 = {} #harga satuan
            

            serpis = []
            sperpart = []
            harga_total_peritem = []
                    
            for i in appointment.services.all():
                serpis.append(i)
                for c in i.kebutuhan_spare_part.all():
                    if c not in sperpart:
                        sperpart.append(c)
                    tampung3[c.nama] = c.harga 

            cursor = connection.cursor()
            cursor.execute("SET search_path TO public")           
            for i in range(len(serpis)):
                cursor.execute(
                    'SELECT * FROM public."services_service_kebutuhan_spare_part" WHERE '
                    '"services_service_kebutuhan_spare_part"."service_id"=%s',
                    [serpis[i].id])
                rows = cursor.fetchall()
                print(len(rows))
                for j in range(len(rows)):
                    if sperpart[j].nama in tampung1.keys():
                        angka = rows[j][3] + tampung1[sperpart[j].nama]
                        tampung1[sperpart[j].nama] = angka
                    else:
                        tampung1[sperpart[j].nama] = rows[j][3] #buat kuantitas
                        

            for k in range(len(sperpart)):
                if sperpart[k].nama in tampung2:
                    total = tampung2[sperpart[k].nama]
                    total += sperpart[k].harga * tampung1[sperpart[k].nama]
                    harga_total_peritem.append(total)
                else:
                    tampung2[sperpart[k].nama] = sperpart[k].harga * tampung1[sperpart[k].nama]
                    harga_total_peritem.append(sperpart[k].harga * tampung1[sperpart[k].nama])

            if form.is_valid():
                form.save()
                return redirect("/nota/")

            response = {
                'form': form,
                'nota_barang': nota_barang,
                'username':request.session['username'],               
                'jabatan':request.session['jabatan'],
                'nota_barang': nota_barang,
                'pelanggan' : pelanggan,
                'nomor_pkb' : nomor_pkb,
                'username': request.session['username'],
                'jabatan': request.session['jabatan'],
                'nomor_polisi' : nomor_polisi,
                'tanggal' : tanggal,
                'sperpart': sperpart,
                'serpis': serpis,
                'tampung1' : tampung1,
                'tampung2' : tampung2,
                'tampung3' : tampung3,
            }

            return render(request, "ceklis-notabarang.html", response)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")
