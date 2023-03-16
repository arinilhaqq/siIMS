from django.shortcuts import render
from django.http import HttpResponse

def create_pelanggan(request):
    first_name = 'Hideng'
    last_name = 'Cihahem'

    context = {
        'first_name':first_name,
        'last_name':last_name,
    }

    return render(request, "create-pelanggan.html", context)