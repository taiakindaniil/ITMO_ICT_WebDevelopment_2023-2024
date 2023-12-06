from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, Http404 
from .models import CarOwner, Car

def owner_detail(request: HttpRequest, owner_id: int) -> HttpResponse:
    try:
        owner = CarOwner.objects.get(pk=owner_id)
    except CarOwner.DoesNotExist:
        raise Http404("Owner does not exist")
    return render(request, 'owner.html', {'owner': owner})


def owner_list(request: HttpRequest) -> HttpResponse:
    return render(request, 'owner_list.html', {'owners': CarOwner.objects.all()})


class CarList(ListView):
    model = Car
    template_name = 'car_list.html'


class CarRetrieveView(DetailView):
    model = Car
    template_name = 'car.html'
