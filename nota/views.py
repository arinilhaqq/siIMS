from django.http import HttpResponseRedirect
from django.shortcuts import render
from appointment.models import Appointment
from datetime import date

def is_authenticated(request):
    try:
        request.session['username']
        return True
    except:
        return False


def nota_list(request):
    if is_authenticated(request):
        if request.session['jabatan'] == 'Akuntan' or request.session['jabatan'] == 'Admin':
            appointment = Appointment.objects.filter(status='Finished').prefetch_related('pelanggan')

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


def receipt_view(request):
    services = [
        {'name': 'Service A', 'price': 100.00},
        {'name': 'Service B', 'price': 50.00},
        {'name': 'Service C', 'price': 75.00}
    ]
    total_price = 225.00

    context = {
        'services': services,
        'total_price': total_price
    }

    return render(request, 'notajasa.html', context)

def barang_view(request):
    # appointment = Appointment.objects.get(id=id)
    # nomor_pkb = appointment.pelanggan.nomor_pkb
    # nomor_polisi = appointment.pelanggan.nomor_polisi
    # tanggal = date.today()
    # pelanggan = appointment.pelanggan.nama_pelanggan
    #
    # print(appointment.services.kebutuhan_spare_part)

    barang = [
        {'nama': 'Baut', 'banyak': 2, 'harga_satuan': 3000, 'harga_total': 6000},
        {'nama': 'Aki', 'banyak': 1, 'harga_satuan': 5000, 'harga_total': 5000},
        {'nama': 'Oli', 'banyak': 4, 'harga_satuan': 2000, 'harga_total': 8000}
    ]

    total_price = 19000

    context = {
        'barang': barang,
        'total_price': total_price
    }

    return render(request, 'notabarang.html', context)

def gabungan_view(request):
    # appointment = Appointment.objects.get(id=id)
    # nomor_pkb = appointment.pelanggan.nomor_pkb
    # nomor_polisi = appointment.pelanggan.nomor_polisi
    # tanggal = date.today()
    # pelanggan = appointment.pelanggan.nama_pelanggan
    #
    # print(appointment.services.kebutuhan_spare_part)

    Nomor_nota_jasa= "XXXXYYYY"
    Nomor_nota_barang= "XXXXYYYY"
    keterangan_lain_lain = "LalalaUwuwuw"
    total_harga_sparepart = 20000
    total_harga_service = 20000
    total_harga_lainlain = 40000

    total_harga_gabungan = 10000

    harga_terbilang = "sepuluh ribuww"


    context = {
        'Nomor_nota_jasa': Nomor_nota_jasa,
        'Nomor_nota_barang': Nomor_nota_barang,
        'keterangan_lain_lain' : keterangan_lain_lain,
        'total_harga_sparepart' : total_harga_sparepart,
        'total_harga_service' : total_harga_service,
        'total_harga_lainlain' : total_harga_lainlain,

        'total_harga_gabungan' : total_harga_gabungan,

        'harga_terbilang' : harga_terbilang,
    }

    return render(request, 'notagabungan.html', context)
