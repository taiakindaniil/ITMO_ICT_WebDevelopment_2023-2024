from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, Http404 
from .models import CarOwner, Car
from .forms import CarOwnerForm

def owner_detail(request: HttpRequest, owner_id: int) -> HttpResponse:
    try:
        owner = CarOwner.objects.get(pk=owner_id)
    except CarOwner.DoesNotExist:
        raise Http404("Owner does not exist")
    return render(request, 'owner.html', {'owner': owner})


def owner_list(request: HttpRequest) -> HttpResponse:
    return render(request, 'owner_list.html', {'owners': CarOwner.objects.all()})


def owner_create(request: HttpRequest) -> HttpResponse:
    form = CarOwnerForm(request.POST or None)
    
    if form.is_valid():
        form.save()

    return render(request, 'owner_create.html', {'form': form})


class CarList(ListView):
    model = Car
    template_name = 'car_list.html'


class CarRetrieveView(DetailView):
    model = Car
    template_name = 'car.html'


class CarCreateView(CreateView):
    model = Car
    template_name = 'car_create.html'
    fields = ['model', 'number', 'color']
    success_url = '/cars/'


class CarUpdateView(UpdateView):
    model = Car
    template_name = 'car_update.html'
    fields = ['model', 'number', 'color']
    success_url = '/cars/'


class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_delete.html'
    success_url = '/cars/'