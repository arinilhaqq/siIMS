from django.shortcuts import render, redirect
from .models import Pelanggan
from .forms import PelangganForm, PelangganSearchForm, PelangganSortForm
from django.http import HttpResponseRedirect

def is_authenticated(request):
    try:
        request.session['username']
        return True
    except:
        return False

def pelanggan_list(request):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan' and request.session['jabatan'] !='Inventori' and request.session['jabatan'] !='Teknisi':
            pelanggan = Pelanggan.objects.all().values()  

            form = PelangganSearchForm(request.GET)
            form_sort = PelangganSortForm(request.GET)
            
            response = {'pelanggan': pelanggan, 'username':request.session['username'], 'jabatan':request.session['jabatan']}

            if form.is_valid():
                search_query = form.cleaned_data.get('search_query')
                
                if search_query:
                    pelanggan = pelanggan.filter(nama_pelanggan__icontains=search_query) | pelanggan.filter(telepon_pelanggan__icontains=search_query)
                    
            if form_sort.is_valid():
                pilihan = form_sort.cleaned_data.get('pilihan')

                if pilihan:
                    if pilihan == 'Terbaru':
                        pelanggan = pelanggan.order_by("-id")
                    elif pilihan == 'Terlama':
                        pelanggan = pelanggan.order_by("id")

            response = {
                "form": form,
                'form_sort': form_sort,
                "pelanggan": pelanggan,
                'username':request.session['username'], 
                'jabatan':request.session['jabatan']
            }

            return render(request, 'pelanggan_list.html', response)
        else:
            return HttpResponseRedirect ("/")
    else:
        return HttpResponseRedirect("/login")

def create_pelanggan(request):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan' and request.session['jabatan'] !='Inventori' and request.session['jabatan'] !='Teknisi':
            context = {}

            form = PelangganForm(request.POST or None)
            if (form.is_valid() and request.method == 'POST'):
                form.save()
                return redirect('/list-pelanggan/')

            context['form'] = form
            context['username'] = request.session['username']
            context['jabatan'] = request.session['jabatan']
            return render(request, 'create-pelanggan.html', context)
        else:
            return HttpResponseRedirect ("/")
    else:
        return HttpResponseRedirect("/login")

def delete_pelanggan(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan' and request.session['jabatan'] !='Inventori'and request.session['jabatan'] !='Teknisi':
            pelanggan_by_id = Pelanggan.objects.get(id=id)
            pelanggan_by_id.delete()

            pelanggan = Pelanggan.objects.all().values()  
            response = {'pelanggan': pelanggan, 'username':request.session['username'], 'jabatan':request.session['jabatan']}
            return render(request, 'pelanggan_list.html', response)
        else:
            return HttpResponseRedirect ("/")
    else:
            return HttpResponseRedirect("/login")

def detail_pelanggan(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan' and request.session['jabatan'] !='Inventori'and request.session['jabatan'] !='Teknisi':
            pelanggan = Pelanggan.objects.get(id=id)

            response = {'pelanggan': pelanggan, 'username':request.session['username'], 'jabatan':request.session['jabatan']}
            return render(request, 'pelanggan_list.html', response)
        else:
            return HttpResponseRedirect ("/")
    else:
        return HttpResponseRedirect("/login")

def update_pelanggan(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan' and request.session['jabatan'] !='Inventori'and request.session['jabatan'] !='Teknisi':
            pelanggan = Pelanggan.objects.get(id=id)
            response = {'pelanggan': pelanggan, 'username':request.session['username'], 'jabatan':request.session['jabatan']}
            if request.method == 'POST':
                form = PelangganForm(request.POST, instance=pelanggan)
                if form.is_valid():
                    form.save()
                return redirect('/list-pelanggan/')
            return render(request, "update-pelanggan.html", response)
        else:
            return HttpResponseRedirect ("/")
    else:
        return HttpResponseRedirect("/login")