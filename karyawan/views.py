from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Karyawan
from .forms import KaryawanForm


def create_karyawan(request):
    context = {}

    form = KaryawanForm(request.POST or None)
    if (form.is_valid() and request.method == 'POST'):
        form.save()
        return redirect('/list-karyawan/')
    
    context['form'] = form

    return render(request, "create-karyawan.html", context)

def karyawan_list(request):
    karyawan = Karyawan.objects.all().values()
    response = {'karyawan': karyawan}
    return render(request, 'karyawan-list.html', response)

def detail_karyawan(request, id):
    karyawan_by_id = Karyawan.objects.get(id=id)
    response = {'karyawan': karyawan_by_id}
    return render(request, 'detail-karyawan.html', response)

def delete_karyawan(request, id):
    karyawan_by_id = Karyawan.objects.get(id=id)
    karyawan_by_id.delete()

    karyawan = Karyawan.objects.all().values()
    response = {'karyawan': karyawan}
    return render(request, 'karyawan-list.html', response)