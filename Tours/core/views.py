from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.models import User

from core.utils import *
from core.models import *
from django.db.models import Q

import csv # debug

def index(request):
    randomize_booking_weights()

    return redirect('core:change-island', island='Oahu')

def change_island(request, island):
    island = Island.objects.get(name=island)
    bookings = Booking.objects.filter(island=island).order_by('-weight')
    page_number = int(request.GET.get('page',1))
    paginator = Paginator(bookings, 6)
    page_obj = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(page_number, on_each_side=0, on_ends=1)

    context = {
        'page_obj' : page_obj,
        'tours': get_tours(island),
        'activities': get_activities(island),
        'islands': Island.objects.all(),
        'current_island':island,
        'current_category' : None,
        'page_range': page_range,
    }

    if page_number == 1:
        collage = get_collage()
        context.update(collage)
    return render(request, 'core/base_site.html', context)


def change_category(request, island, category):
    try:
        island = Island.objects.get(name=island)
    except Island.DoesNotExist:
        return redirect('/')

    # If category is type instead of category, get all in that type
    if Type.objects.filter(name=category).exists():
        type = get_object_or_404(Type, name=category)
        bookings = Booking.objects.filter(island=island, category__type=type).order_by('-weight')
        if category == 'tour':
            category = 'All Tours'
        else:
            category = 'All Activities'
    else:
        category = Category.objects.get(name=category)
        bookings = Booking.objects.filter(island=island).filter(category=category).order_by('-weight')

    paginator = Paginator(bookings, 6)
    page_number = int(request.GET.get('page',1))
    page_obj = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(page_number, on_each_side=1, on_ends=1)


    context = {
        'page_obj' : page_obj,
        'tours': get_tours(island),
        'activities': get_activities(island),
        'islands':Island.objects.all(),
        'current_island':island,
        'current_category':category,
        'page_range': page_range,
    }

    if page_number == 1:
        collage = get_collage()
        context.update(collage)
    return render(request, 'core/base_site.html', context)


def get_search(request, island):
    try:
        island = Island.objects.get(name=island)
    except Island.DoesNotExist:
        return redirect('/')
    
    query = request.GET.get('q', '')
    if request.user.is_authenticated:
        return redirect(f'/{island}/search?q={query}')
    elif SearchQuery.objects.filter(query=query, island=island).exists():
        results = len(Booking.objects.filter( Q(title__icontains=query) | Q(company_name__icontains=query) | Q(city__icontains=query) | Q(fareharbor_item_id__icontains=query) | Q(category__name__icontains=query), island=island ))
        SearchQuery.objects.create(query=query, island=island, results=results)
        updated_search_queries =[]
        search_queries = SearchQuery.objects.filter(query=query, island=island)
        new_count = len(SearchQuery.objects.filter(query=query, island=island))
        for search_query in search_queries:
            search_query.count = new_count
            updated_search_queries.append(search_query)
        SearchQuery.objects.bulk_update(updated_search_queries, ['count'])
    else:
        results = len(Booking.objects.filter( Q(title__icontains=query) | Q(company_name__icontains=query) | Q(city__icontains=query) | Q(fareharbor_item_id__icontains=query) | Q(category__name__icontains=query), island=island ))
        SearchQuery.objects.create(query=query, island=island, results=results)
    return redirect(f'/{island}/search?q={query}')

def search_results(request, island):
    island = Island.objects.get(name=island)
    query = request.GET.get('q', '')

    bookings = Booking.objects.filter( Q(title__icontains=query) | Q(company_name__icontains=query) | Q(city__icontains=query) | Q(fareharbor_item_id__icontains=query) | Q(category__name__icontains=query), island=island )

    paginator = Paginator(bookings, 6)
    page_number = int(request.GET.get('page',1))
    page_obj = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(page_number, on_each_side=1, on_ends=1)


    context = {
        'page_obj' : page_obj,
        'tours': get_tours(island),
        'activities': get_activities(island),
        'islands':Island.objects.all(),
        'current_island':island,
        'current_category': query,
        'page_range': page_range,
        'query':query,
    }
    return render(request, 'core/search.html', context)

