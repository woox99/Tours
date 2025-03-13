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
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(island=island).order_by('fh_id')
    else:
        bookings = Booking.objects.filter(island=island, is_public=True).order_by('-weight')
    page_obj, page_range = paginate_bookings(bookings, request)

    context = {
        'page_obj' : page_obj,
        'tours': get_tours(island),
        'activities': get_activities(island),
        'categories': Category.objects.all().order_by('name'),
        'islands': Island.objects.all(),
        'current_island':island,
        'current_category' : None,
        'breadcrumb' : None,
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
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(island=island).filter(category=category).order_by('fh_id')
    else:
        bookings = Booking.objects.filter(island=island, is_public=True).filter(category=category).order_by('-weight')
    page_obj, page_range = paginate_bookings(bookings, request)

    context = {
        'page_obj' : page_obj,
        'tours': get_tours(island),
        'activities': get_activities(island),
        'categories': Category.objects.all().order_by('name'),
        'islands':Island.objects.all(),
        'current_island':island,
        'current_category':category,
        'breadcrumb' : category,
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
        Q(fh_id__icontains=query) | 
        Q(category__name__icontains=query), 
        island=island,
        is_public=True,
    ).count()
    new_search_query.results = results
    new_search_query.save()

    return redirect(reverse('core:search-results', kwargs={'island': island.name}) + f'?q={query}')


def search_results(request, island):
    island = get_object_or_404(Island, name=island)
    query = request.GET.get('q', '')
    if request.user.is_authenticated:
        bookings = Booking.objects.filter( 
            Q(title__icontains=query) | 
            Q(company_name__icontains=query) | 
            Q(city__icontains=query) | 
            Q(fh_id__icontains=query) | 
            Q(category__name__icontains=query), 
            island=island,
        )
    else:
        bookings = Booking.objects.filter( 
            Q(title__icontains=query) | 
            Q(company_name__icontains=query) | 
            Q(city__icontains=query) | 
            Q(fh_id__icontains=query) | 
            Q(category__name__icontains=query), 
            island=island,
            is_public=True,
        )
    page_obj, page_range = paginate_bookings(bookings, request)

    context = {
        'page_obj' : page_obj,
        'tours': get_tours(island),
        'activities': get_activities(island),
        'categories': Category.objects.all().order_by('name'),
        'islands':Island.objects.all(),
        'current_island':island,
        'current_category': None,
        'breadcrumb' : query,
        'page_range': page_range,
        'query':query,
    }
    return render(request, 'core/search.html', context)


def tours(request, island):
    island = get_object_or_404(Island, name=island)
    type = get_object_or_404(Type, name='Tour')
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(category__type=type, island=island).order_by('fh_id')
    else:
        bookings = Booking.objects.filter(category__type=type, island=island, is_public=True).order_by('-weight')

    page_obj, page_range = paginate_bookings(bookings, request)

    context = {
        'page_obj' : page_obj,
        'tours': get_tours(island),
        'activities': get_activities(island),
        'categories': Category.objects.all().order_by('name'),
        'islands':Island.objects.all(),
        'current_island':island,
        'current_category': 'tours',
        'breadcrumb' : 'All Tours',
        'page_range': page_range,
    }

    if page_obj.number == 1:
        context.update(get_collage())
    return render(request, 'core/base_site.html', context)


def activities(request, island):
    island = get_object_or_404(Island, name=island)
    type = get_object_or_404(Type, name='Activity')
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(category__type=type, island=island).order_by('fh_id')
    else:
        bookings = Booking.objects.filter(category__type=type, island=island, is_public=True).order_by('-weight')
    page_obj, page_range = paginate_bookings(bookings, request)

    context = {
        'page_obj' : page_obj,
        'tours': get_tours(island),
        'activities': get_activities(island),
        'categories': Category.objects.all().order_by('name'),
        'islands':Island.objects.all(),
        'current_island':island,
        'current_category': 'activities',
        'breadcrumb' : 'All Activities',
        'page_range': page_range,
    }

    if page_obj.number == 1:
        context.update(get_collage())
    return render(request, 'core/base_site.html', context)


def booking_update(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.title = request.POST['title']
    booking.category = get_object_or_404(Category, pk=request.POST['category_id'])
    booking.is_public = True if request.POST['is_public'] == 'true' else False
    if booking.is_public:
        booking.is_verified = True
    booking.save()

    island=request.POST['current_island']
    page_number = request.POST['page_number']
    if request.POST['current_category'] == 'None':
        return redirect(reverse('core:island-results', kwargs={'island': island}) + f'?page={page_number}' + f'#{booking.fh_id}')
    category = request.POST['current_category']
    return redirect(reverse('core:category-results', kwargs={'island': island, 'category':category}) + f'?page={page_number}' + f'#{booking.fh_id}')


def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.delete()

    island=request.POST['current_island']
    page_number = request.POST['page_number']
    if request.POST['current_category'] == 'None':
        return redirect(reverse('core:island-results', kwargs={'island': island}) + f'?page={page_number}')
    category = request.POST['current_category']
    return redirect(reverse('core:category-results', kwargs={'island': island, 'category':category}) + f'?page={page_number}')