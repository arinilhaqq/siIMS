from django.shortcuts import render
from django.http import HttpResponse

def create_karyawan(request):
    first_name = 'Ini'
    last_name = 'Karyawan'

    context = {
        'first_name':first_name,
        'last_name':last_name,
    }

    return render(request, "create-karyawan.html", context)