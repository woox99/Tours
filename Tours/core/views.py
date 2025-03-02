from django.shortcuts import render, get_object_or_404, redirect
from core.utils import get_collage
from django.core.paginator import Paginator


from core.models import *

import csv # debug


# Create your views here.
def index(request):

    # if session
    island = Island.objects.filter(name='Oahu').first()

    bookings = Booking.objects.filter(island=island)
    paginator = Paginator(bookings, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj' : page_obj,
        'tours':Category.objects.filter(type=get_object_or_404(Type, name='Tour')).order_by('name'),
        'activities':Category.objects.filter(type=get_object_or_404(Type, name='Activity')).exclude(name='Other').order_by('name'),
        'islands':Island.objects.all(),
        'current_island':island,
        'current_category' : None,
    }
    if page_number == str(1) or page_number == None:
        collage = get_collage()
        context.update(collage)
    return render(request, 'core/base_site.html', context)


def change_island(request, island):
    island = Island.objects.filter(name=island).first()
    
    bookings = Booking.objects.filter(island=island)
    paginator = Paginator(bookings, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj' : page_obj,
        'tours':Category.objects.filter(type=get_object_or_404(Type, name='Tour')).order_by('name'),
        'activities':Category.objects.filter(type=get_object_or_404(Type, name='Activity')).exclude(name='Other').order_by('name'),
        'islands':Island.objects.all(),
        'current_island':island,
        'current_category' : None,
    }
    if page_number == str(1) or page_number == None:
        collage = get_collage()
        context.update(collage)
    return render(request, 'core/base_site.html', context)


def change_category(request, island, category):
    island = Island.objects.filter(name=island).first()

    # If category is type instead of category, get all in that type
    if Type.objects.filter(name=category).exists():
        type = get_object_or_404(Type, name=category)
        bookings = Booking.objects.filter(island=island, category__type=type)
        if category == 'tour':
            category = 'All Tours'
        else:
            category = 'All Activities'
    else:
        category = Category.objects.filter(name=category).first()
        bookings = Booking.objects.filter(island=island).filter(category=category)

    paginator = Paginator(bookings, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj' : page_obj,
        'tours':Category.objects.filter(type=get_object_or_404(Type, name='Tour')).order_by('name'),
        'activities':Category.objects.filter(type=get_object_or_404(Type, name='Activity')).exclude(name='Other').order_by('name'),
        'islands':Island.objects.all(),
        'current_island':island,
        'current_category':category,
    }
    if page_number == str(1) or page_number == None:
        collage = get_collage()
        context.update(collage)
    return render(request, 'core/base_site.html', context)
