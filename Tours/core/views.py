from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator



from core.utils import *
from core.models import *
from django.db.models import Q



import csv # debug

def index(request):
    # Randomizes bookings weights if booking hasn't been clicked in 1 days
    randomize_booking_weights()
    return redirect('core:home')

def home(request):

    island = Island.objects.filter(name='Oahu').first()

    bookings = Booking.objects.filter(island=island).order_by('-weight')
    paginator = Paginator(bookings, 6)
    page_number = int(request.GET.get('page',1))
    page_obj = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(page_number, on_each_side=1, on_ends=1)

    context = {
        'page_obj' : page_obj,
        'tours':Category.objects.filter(type=get_object_or_404(Type, name='Tour')).order_by('name'),
        'activities':Category.objects.filter(type=get_object_or_404(Type, name='Activity')).exclude(name='Other').order_by('name'),
        'islands':Island.objects.all(),
        'current_island':island,
        'current_category' : None,
        'page_range': page_range,
    }
    if page_number == 1 or page_number == None:
        collage = get_collage()
        context.update(collage)
    return render(request, 'core/base_site.html', context)


def change_island(request, island):

    island = Island.objects.filter(name=island).first()
    
    bookings = Booking.objects.filter(island=island).order_by('-weight')
    paginator = Paginator(bookings, 6)
    page_number = int(request.GET.get('page',1))
    page_obj = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(page_number, on_each_side=0, on_ends=1)


    context = {
        'page_obj' : page_obj,
        'tours':Category.objects.filter(type=get_object_or_404(Type, name='Tour')).order_by('name'),
        'activities':Category.objects.filter(type=get_object_or_404(Type, name='Activity')).exclude(name='Other').order_by('name'),
        'islands':Island.objects.all(),
        'current_island':island,
        'current_category' : None,
        'page_range': page_range,

    }
    if page_number == 1 or page_number == None:
        collage = get_collage()
        context.update(collage)
    return render(request, 'core/base_site.html', context)


def change_category(request, island, category):
    island = Island.objects.filter(name=island).first()

    # If category is type instead of category, get all in that type
    if Type.objects.filter(name=category).exists():
        type = get_object_or_404(Type, name=category)
        bookings = Booking.objects.filter(island=island, category__type=type)
        bookings = Booking.objects.filter(island=island, category__type=type).order_by('-weight')
        if category == 'tour':
            category = 'All Tours'
        else:
            category = 'All Activities'
    else:
        category = Category.objects.filter(name=category).first()
        bookings = Booking.objects.filter(island=island).filter(category=category).order_by('-weight')

    paginator = Paginator(bookings, 6)
    page_number = int(request.GET.get('page',1))
    page_obj = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(page_number, on_each_side=1, on_ends=1)


    context = {
        'page_obj' : page_obj,
        'tours':Category.objects.filter(type=get_object_or_404(Type, name='Tour')).order_by('name'),
        'activities':Category.objects.filter(type=get_object_or_404(Type, name='Activity')).exclude(name='Other').order_by('name'),
        'islands':Island.objects.all(),
        'current_island':island,
        'current_category':category,
        'page_range': page_range,

    }
    if page_number == 1 or page_number == None:
        collage = get_collage()
        context.update(collage)
    return render(request, 'core/base_site.html', context)


def search(request, island):
    island = Island.objects.filter(name=island).first()

    query = request.GET.get('q', '')
    bookings = Booking.objects.filter( Q(title__icontains=query) | Q(company_name__icontains=query) | Q(city__icontains=query) | Q(fareharbor_item_id__icontains=query) | Q(category__name__icontains=query), island=island )

    paginator = Paginator(bookings, 6)
    page_number = int(request.GET.get('page',1))
    page_obj = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(page_number, on_each_side=1, on_ends=1)


    context = {
        'page_obj' : page_obj,
        'tours':Category.objects.filter(type=get_object_or_404(Type, name='Tour')).order_by('name'),
        'activities':Category.objects.filter(type=get_object_or_404(Type, name='Activity')).exclude(name='Other').order_by('name'),
        'islands':Island.objects.all(),
        'current_island':island,
        'current_category': query,
        'page_range': page_range,
        'query':query,
    }
    return render(request, 'core/search.html', context)

