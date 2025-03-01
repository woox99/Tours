from django.shortcuts import render, get_object_or_404, redirect
from core.utils import get_collage

from core.models import *

import csv # debug


# Create your views here.
def index(request):

    # if session
    island = Island.objects.filter(name='Oahu').first()
    bookings = Booking.objects.filter(island=island).order_by('?')[:6]

    context = {
        'bookings' : bookings,
        'tours':Category.objects.filter(type=get_object_or_404(Type, name='Tour')).order_by('name'),
        'activities':Category.objects.filter(type=get_object_or_404(Type, name='Activity')).exclude(name='Other').order_by('name'),
        'islands':Island.objects.all(),
        'current_island':island,
    }
    collage = get_collage()
    context.update(collage)
    return render(request, 'core/base_site.html', context)


def change_island(request, island):
    island = Island.objects.filter(name=island).first()
    bookings = Booking.objects.filter(island=island).order_by('?')[:6]

    context = {
        'bookings' : bookings,
        'tours':Category.objects.filter(type=get_object_or_404(Type, name='Tour')).order_by('name'),
        'activities':Category.objects.filter(type=get_object_or_404(Type, name='Activity')).exclude(name='Other').order_by('name'),
        'islands':Island.objects.all(),
        'current_island':island,
    }
    collage = get_collage()
    context.update(collage)
    return render(request, 'core/base_site.html', context)