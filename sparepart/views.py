from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .models import SparePart
from services.models import Service
from .forms import SparePartForm
# from django.core.paginator import Paginator

def is_authenticated(request):
    try:
        request.session['username']
        return True
    except:
        return False


def sparepart_list(request):
    if is_authenticated(request):
        if request.session['jabatan'] != 'Akuntan':
            # sparepart = SparePart.objects.all().values()
            sparepart = SparePart.objects.prefetch_related('services').all()
            response = {'sparepart': sparepart, 'username': request.session['username'],
                        'jabatan': request.session['jabatan']}
            return render(request, 'list-spare-part.html', response)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")


def add_sparepart(request):
    if is_authenticated(request):
        if request.session['jabatan'] != 'Akuntan':
            context = {}

            form = SparePartForm(request.POST or None)
            # queryset = form.fields['services'].queryset
            # objects_per_page = 10
            # paginator = Paginator(queryset, objects_per_page)
            # current_page_objects = paginator.get_page(page_number).object_list
            if (form.is_valid() and request.method == 'POST'):
                form.save()
                # sparepart = form.save()  # save the book with the selected authors
                # services = sparepart.services.all()  # get the selected authors
                # print(services)
                return redirect('/list-sparepart')

            context['form'] = form
            context['username'] = request.session['username']
            context['jabatan'] = request.session['jabatan']
            return render(request, 'create-spare-part.html', context)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")


def detail_sparepart(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] != 'Akuntan':
            context = {}
            context["data"] = SparePart.objects.get(id=id)
            context['username'] = request.session['username']
            context['jabatan'] = request.session['jabatan']
            return render(request, "list-spare-part.html", context)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")


def delete_sparepart(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] != 'Akuntan':
            sparepart = SparePart.objects.get(id=id)
            sparepart.delete()
            spareparts = SparePart.objects.all().values()
            response = {'spareparts': spareparts, 'username': request.session['username'],
                        'jabatan': request.session['jabatan']}
            return render(request, 'list-spare-part.html', response)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")


def update_sparepart(request, id):
    if is_authenticated(request):
        if request.session['jabatan'] != 'Akuntan':
            obj = get_object_or_404(SparePart, id=id)
            form = SparePartForm(request.POST or None, instance=obj)
            if form.is_valid():
                form.save()
                return redirect('/list-sparepart')
            response = {'form': form, 'sparepart': obj, 'username': request.session['username'],
                        'jabatan': request.session['jabatan']}
            return render(request, "update-spare-part.html", response)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")