from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Karyawan
from .forms import KaryawanForm, KaryawanSearchForm

def is_authenticated(request):
    try:
        request.session['username']
        return True
    except:
        return False
    
def create_karyawan(request):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan' and request.session['jabatan'] !='Inventori'and request.session['jabatan'] !='Teknisi' and request.session['jabatan'] !='Service Advisor':
            context = {}
            username = request.session['username']
            context['username'] = request.session['username']
            context['jabatan'] = request.session['jabatan']
            form = KaryawanForm(request.POST or None)
            context['form'] = form
            if (form.is_valid() and request.method == 'POST'):
                username = request.POST['username']
                if Karyawan.objects.filter(username=username).exists():
                    messages.error(request, 'Username sudah dipakai')
                else:
                    form.save()
                    return redirect('/list-karyawan/')
            return render(request, "create-karyawan.html", context)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")

def karyawan_list(request):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan'and request.session['jabatan'] !='Inventori'and request.session['jabatan'] !='Teknisi' and request.session['jabatan'] !='Service Advisor':
            karyawan = Karyawan.objects.all().values()

            form = KaryawanSearchForm(request.GET)

            response = {'karyawan': karyawan, 'username':request.session['username'], 'jabatan':request.session['jabatan'], 'form': form}
            
            if form.is_valid():
                search_query = form.cleaned_data.get('search_query')
                
                if search_query:
                    karyawan = karyawan.filter(nama_karyawan__icontains=search_query) | karyawan.filter(jabatan__icontains=search_query)
                    
            response = {
                "form": form,
                "karyawan": karyawan,
                'username':request.session['username'], 
                'jabatan':request.session['jabatan']
            }
                    
            return render(request, 'karyawan-list.html', response)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")

def detail_karyawan(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan' and request.session['jabatan'] !='Inventori'and request.session['jabatan'] !='Teknisi' and request.session['jabatan'] !='Service Advisor':
            karyawan_by_id = Karyawan.objects.get(id=id)
            response = {'karyawan_by_id': karyawan_by_id, 'username':request.session['username'], 'jabatan':request.session['jabatan']}
            return render(request, 'karyawan-list.html', response)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")

def delete_karyawan(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan' and request.session['jabatan'] !='Inventori'and request.session['jabatan'] !='Teknisi' and request.session['jabatan'] !='Service Advisor':
            karyawan_by_id = Karyawan.objects.get(id=id)
            karyawan_by_id.delete()

            karyawan = Karyawan.objects.all().values()
            response = {'karyawan': karyawan, 'username':request.session['username'], 'jabatan':request.session['jabatan']}
            return render(request, 'karyawan-list.html', response)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")

def update_karyawan(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] !='Akuntan' and request.session['jabatan'] !='Inventori'and request.session['jabatan'] !='Teknisi' and request.session['jabatan'] !='Service Advisor':
            context = {}
            karyawan = Karyawan.objects.get(id=id)
            context['karyawan']=karyawan
            
            form = KaryawanForm(request.POST, instance=karyawan)
            print(form.is_valid()) # False
            if (form.is_valid() and request.method == 'POST'):
                form.save()
                return redirect('/list-karyawan/')
            context['form'] = form
            context['username'] = request.session['username']
            context['jabatan'] = request.session['jabatan']
            return render(request, 'update-karyawan.html', context)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")
    
# def search_karyawan(request):
#     query = request.GET.get('search_query')
#     results = Karyawan.objects.filter(nama_karyawan__icontains=query) | Karyawan.objects.filter(content__icontains=query)
#     context = {'results': results}
#     return render(request, 'search_results_karyawan.html', context)
