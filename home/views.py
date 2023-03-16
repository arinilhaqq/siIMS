from django.shortcuts import render
from django.http import HttpResponse

def homepage(request):
    first_name = 'Jajang'
    last_name = 'Meyon'

    context = {
        'first_name':first_name,
        'last_name':last_name,
    }

    return render(request, "homepage.html", context)
