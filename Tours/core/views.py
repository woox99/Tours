from django.shortcuts import render, get_object_or_404
from core.utils import get_collage

from core.models import *

import csv # debug


# Create your views here.
def index(request):



    collage = get_collage()
    context = {
        'bookings' : Booking.objects.all()[:6],
        'tours':Category.objects.filter(type=get_object_or_404(Type, name='Tour')).order_by('name'),
        'activities':Category.objects.filter(type=get_object_or_404(Type, name='Activity')).exclude(name='Other').order_by('name'),
    }
    context.update(collage)
    return render(request, 'core/base_site.html', context)