from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

def is_authenticated(request):
    try:
        request.session['username']
        return True
    except:
        return False

def homepage(request):
    print(is_authenticated)
    if is_authenticated(request):
        context = {}
        context['username'] = request.session['username']
        if request.session['jabatan'] =='Owner'|request.session['jabatan'] =='Akuntan'|request.session['jabatan'] =='Inventori'|request.session['jabatan'] =='Teknisi'|request.session['jabatan'] =='Service Advisor':
            return render(request, 'homepage.html', context)
    else:
        return HttpResponseRedirect("/login")