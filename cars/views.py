from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Max, Min, F, Q
from . import models, forms

# Create your views here.
def index(request):
    cars = models.Car.objects.order_by("order")
    return render(request, "cars/index.html", locals())

def create(request):
    car = models.Car()
    form = forms.Car()
    if request.method == "POST":
        mx = models.Car.objects.aggregate(Max("order"))
        order = mx["order__max"] if mx["order__max"] is not None else -1
        car = models.Car(
            name=request.POST["name"],
            color=request.POST["color"],
            order=order + 1
        )
        form = forms.Car(dict(name=car.name, color=car.color))
        if form.is_valid():
            try:
                car.validate_unique()
                car.save()
                return redirect("index")
            except:
                pass
    return render(request, "cars/create.html", locals())

def update(request, id):
    car = models.Car.objects.get(id=id)
    form = forms.Car(dict(name=car.name, color=car.color))
    if request.method == "POST":
        form = forms.Car(dict(name=car.name, color=car.color))
        if form.is_valid():
            models.Car.objects.filter(id=car.id).update(
                **dict(color=request.POST["color"]))
            return redirect("index")
    return render(request, "cars/update.html", locals())

def delete(request, id):
    car = models.Car.objects.get(id=id)
    if car:
        car.delete()
        models.Car.objects.filter(order__gt=car.order).update(
            order=F("order") - 1)
    return redirect("index")

def move(request, id, direction=1):
    direction = direction if direction in (-1, 1) else 1
    car = models.Car.objects.get(id=id)
    if direction == -1:
        other = models.Car.objects.filter(order__lt=car.order).aggregate(Max("order"))
        other = other["order__max"]
    elif direction == 1:
        other = models.Car.objects.filter(order__gt=car.order).aggregate(Min("order"))
        other = other["order__min"]
    if other is not None:
        models.Car.objects.filter(~Q(id=car.id), order=other).update(order=car.order)
        models.Car.objects.filter(id=car.id).update(order=other)
    return redirect("index")

def move_up(request, id):
    return move(request, id, -1)

def move_down(request, id):
    return move(request, id, 1)