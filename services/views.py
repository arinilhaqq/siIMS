from django.shortcuts import render
from django.http import HttpResponse

def create_services(request):
    jenis_services = 'Ganti Oli'

    context = {
        'jenis_services': jenis_services
    }

    return render(request, "create-services.html", context)