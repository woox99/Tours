from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User

from core.utils import *
from core.models import *
from django.db.models import Q

from datetime import timedelta 


import csv # debug

def index(request):
    bookings = Booking.objects.filter(modified__lt=now() - timedelta(days=1))
    if bookings:
        randomize_booking_weights(bookings)
    if request.user.is_anonymous:
        ref = request.GET.get('ref', '')
        ref = '?ref=' + ref
        SiteVisit.objects.create(ref=ref)
    return redirect('core:change-island', island='Oahu')


def change_island(request, island):
    island = get_object_or_404(Island, name=island)
    bookings = Booking.objects.filter(island=island).order_by('-weight')
    page_obj, page_range = paginate_bookings(bookings, request)

    context = {
        'page_obj' : page_obj,
        'tours': get_tours(island),
        'activities': get_activities(island),
        'islands': Island.objects.all(),
        'current_island':island,
        'current_category' : None,
        'page_range': page_range,
    }

    if page_obj.number == 1:
        context.update(get_collage())
    return render(request, 'core/base_site.html', context)


def change_category(request, island, category):
    island = get_object_or_404(Island, name=island)
    category = get_object_or_404(Category, name=category)
    bookings = Booking.objects.filter(island=island).filter(category=category).order_by('-weight')
    page_obj, page_range = paginate_bookings(bookings, request)

    context = {
        'page_obj' : page_obj,
        'tours': get_tours(island),
        'activities': get_activities(island),
        'islands':Island.objects.all(),
        'current_island':island,
        'current_category':category,
        'page_range': page_range,
    }

    if page_obj.number == 1:
        context.update(get_collage())
    return render(request, 'core/base_site.html', context)


def search_log(request, island):
    island = get_object_or_404(Island, name=island)
    query = request.GET.get('q', '')

    if request.user.is_authenticated:
        return redirect(f'/{island}/search/?q={query}')
    elif SearchQuery.objects.filter(query=query, island=island).exists():
        new_search_query = SearchQuery.objects.create(query=query, island=island)
        results = len(Booking.objects.filter( Q(title__icontains=query) | Q(company_name__icontains=query) | Q(city__icontains=query) | Q(fareharbor_item_id__icontains=query) | Q(category__name__icontains=query), island=island ))
        new_search_query.results = results
        new_search_query.save()

        updated_search_queries = []
        search_queries = SearchQuery.objects.filter(query=query, island=island)
        new_count = len(search_queries)
        for search_query in search_queries:
            search_query.count = new_count
            updated_search_queries.append(search_query)
        SearchQuery.objects.bulk_update(updated_search_queries, ['count'])
    else:
        new_search_query = SearchQuery.objects.create(query=query, island=island)
        results = len(Booking.objects.filter( Q(title__icontains=query) | Q(company_name__icontains=query) | Q(city__icontains=query) | Q(fareharbor_item_id__icontains=query) | Q(category__name__icontains=query), island=island ))
        new_search_query.results = results
        new_search_query.save()
    return redirect(f'/{island}/search?q={query}')


def search_results(request, island):
    island = get_object_or_404(Island, name=island)
    query = request.GET.get('q', '')
    bookings = Booking.objects.filter( Q(title__icontains=query) | Q(company_name__icontains=query) | Q(city__icontains=query) | Q(fareharbor_item_id__icontains=query) | Q(category__name__icontains=query), island=island )
    page_obj, page_range = paginate_bookings(bookings, request)

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

