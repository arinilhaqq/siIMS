from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
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
        # kebutuhan_spare_part = form.cleaned_data['kebutuhan_spare_part']
        # kuantitas_spare_part = form.cleaned_data['kuantitas_spare_part']
        form.save()
        return redirect('/list-services')

    context['form'] = form
    return render(request, 'create-services.html', context)


def detail_view(request, id):
    context = {}
    context["data"] = Service.objects.get(id=id)
    return render(request, "detail_view_service.html", context)

def delete_service(request, id):
    service = Service.objects.get(id=id)
    service.delete()
    services = Service.objects.all().values()
    response = {'services': services}
    return render(request, 'service_list.html', response)


def update_service(request, id):
    context = {}
    obj = get_object_or_404(Service, id=id)
    form = ServiceForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('/list-services')
    context["form"] = form
    return render(request, "update_view_service.html", context)