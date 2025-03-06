from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.urls import reverse

from core.utils import *
from core.models import *
from django.db.models import Q

from datetime import timedelta 


import csv # debug
import time #debug

def index(request):
    # Randomize weights for bookings that haven't been clicked/updated in days=1
    outdated_bookings = Booking.objects.filter(modified__lt=now() - timedelta(days=1))
    if outdated_bookings:
        randomize_booking_weights(outdated_bookings)
    if request.user.is_anonymous:
        ref = request.GET.get('ref', '')
        ref = '?ref=' + ref
        SiteVisit.objects.create(ref=ref)
    return redirect('core:island-results', island='Oahu')


def change_island(request, island):
    if request.user.is_anonymous:
        log_traffic(instance=get_object_or_404(Island, name=island))
    return redirect('core:island-results', island)


def island_results(request, island):
    island = get_object_or_404(Island, name=island)
    bookings = Booking.objects.filter(island=island).order_by('-weight')
    page_obj, page_range = paginate_bookings(bookings, request)

    context = {
        'page_obj' : page_obj,
        'tours': get_tours(island),
        'activities': get_activities(island),
        'categories': Category.objects.all().order_by('name'),
        'islands': Island.objects.all(),
        'current_island':island,
        'current_category' : None,
        'page_range': page_range,
    }

    if page_obj.number == 1:
        context.update(get_collage())
    return render(request, 'core/base_site.html', context)


def change_category(request, island, category):
    if request.user.is_anonymous:
        log_traffic(instance=get_object_or_404(Category, name=category))
    return redirect('core:category-results', island, category)


def category_results(request, island, category):
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

    # Only logs the search query if user is not an admin
    if request.user.is_authenticated:
        return redirect(reverse('core:search-results', kwargs={'island': island.name}) + f'?q={query}')
    
    search_queries = SearchQuery.objects.filter(query=query, island=island)

    if search_queries.exists():
        query_count = search_queries.count() + 1
        search_queries.update(count=query_count)
    else:
        query_count = 1

    # Save new query
    new_search_query = SearchQuery.objects.create(
        query=query, 
        island=island,
        count=query_count, 
    )
    results = Booking.objects.filter( 
        Q(title__icontains=query) | 
        Q(company_name__icontains=query) | 
        Q(city__icontains=query) | 
        Q(fareharbor_item_id__icontains=query) | 
        Q(category__name__icontains=query), 
        island=island
    ).count()
    new_search_query.results = results
    new_search_query.save()

    return redirect(reverse('core:search-results', kwargs={'island': island.name}) + f'?q={query}')


def search_results(request, island):
    island = get_object_or_404(Island, name=island)
    query = request.GET.get('q', '')
    bookings = Booking.objects.filter( 
        Q(title__icontains=query) | 
        Q(company_name__icontains=query) | 
        Q(city__icontains=query) | 
        Q(fareharbor_item_id__icontains=query) | 
        Q(category__name__icontains=query), 
        island=island 
    )
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


def tours(request, island):
    island = get_object_or_404(Island, name=island)
    type = get_object_or_404(Type, name='Tour')
    bookings = Booking.objects.filter(category__type=type, island=island)

    page_obj, page_range = paginate_bookings(bookings, request)

    context = {
        'page_obj' : page_obj,
        'tours': get_tours(island),
        'activities': get_activities(island),
        'islands':Island.objects.all(),
        'current_island':island,
        'current_category': 'All Tours',
        'page_range': page_range,
    }

    if page_obj.number == 1:
        context.update(get_collage())
    return render(request, 'core/search.html', context)


def activities(request, island):
    island = get_object_or_404(Island, name=island)
    type = get_object_or_404(Type, name='Activity')
    bookings = Booking.objects.filter(category__type=type, island=island)

    page_obj, page_range = paginate_bookings(bookings, request)

    context = {
        'page_obj' : page_obj,
        'tours': get_tours(island),
        'activities': get_activities(island),
        'islands':Island.objects.all(),
        'current_island':island,
        'current_category': 'All Tours',
        'page_range': page_range,
    }

    if page_obj.number == 1:
        context.update(get_collage())
    return render(request, 'core/search.html', context)