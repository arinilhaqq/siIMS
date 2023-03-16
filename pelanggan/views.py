from django.shortcuts import render, redirect
from .models import Pelanggan
from .forms import PelangganForm

def create_pelanggan(request):
    context = {}

    form = PelangganForm(request.POST or None)
    if (form.is_valid() and request.method == 'POST'):
        form.save()
        return redirect('/')

    context['form'] = form
    return render(request, 'create-pelanggan.html', context)
