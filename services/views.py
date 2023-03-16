from django.shortcuts import render, redirect
from .models import Service
from .forms import ServiceForm


def services_list(request):
    services = Service.objects.all().values()  # TODO Implement this
    response = {'services': services}
    return render(request, 'service_list.html', response)

def add_service(request):
    context = {}

    form = ServiceForm(request.POST or None)
    if (form.is_valid() and request.method == 'POST'):
        form.save()
        return redirect('/services')

    context['form'] = form
    return render(request, 'service_form.html', context)
