from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Karyawan
from .forms import KaryawanForm


def create_karyawan(request):
    context = {}

    form = KaryawanForm(request.POST or None)
    if (form.is_valid() and request.method == 'POST'):
        form.save()
        return redirect('/')
    
    context['form'] = form

    return render(request, "create-karyawan.html", context)

def karyawan_list(request):
    karyawan = Karyawan.objects.all().values()
    response = {'karyawan': karyawan}
    return render(request, 'karyawan_list.html', response)
