from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.urls import reverse

from core.utils import *
from core.models import *
from django.db.models import Q

from datetime import timedelta 


import csv # debug
import time #debug

def index(request):

    last_randomized_date = BookingRandomization.objects.last().date
    if now() - last_randomized_date > timedelta(days=1):
        randomize_booking_weights()

    if request.user.is_anonymous:
        ref = request.GET.get('ref', '')
        ref = '?ref=' + ref
        SiteVisit.objects.create(ref=ref)


    # # Import Fareharbor csv data script
    # path = 'core/fh.csv'
    # with open(path, newline='', encoding='utf-8') as csvfile:
    #     reader = csv.DictReader(csvfile)
    #     for row in reader:
    #         # print(reader.fieldnames)

    #         # Create Categories and Types
    #         try:
    #             category = Category.objects.get(name=row["category"])
    #         except Category.DoesNotExist:
    #             try:
    #                 type = Type.objects.get(name=row["item_type"])
    #             except Type.DoesNotExist:
    #                 type = Type.objects.create(name=row["item_type"])
    #             type = Type.objects.get(name=row["item_type"])
    #             category = Category.objects.create(name=row["category"], type=type)

    #         # Create Islands
    #         try:
    #             island = Island.objects.get(name=row["island"])
    #         except Island.DoesNotExist:
    #             island = Island.objects.create(name=row["island"])

    #         # Create Booking
    #         try:
    #             booking = Booking(
    #                 title=row["item_name"],
    #                 company_name=row["company_name"],
    #                 city=row["city"],
    #                 # category=category,
    #                 # type=Type.objects.get(name=row["item_type"]),
    #                 island=island,
    #                 fh_id=int(row["item_id"]),
    #                 referral_link=row["referral_link"],
    #                 image_URL=row["image_URL"],
    #             )
    #             booking.save()
    #             booking.tags.add(category)
    #         except Exception as e:
    #             print(f"Skipping row due to error: {e}")
    return redirect('core:change-island', island='Oahu')

def info(request):

    
    return render(request, 'core/info.html')

def change_island(request, island):
    island = get_object_or_404(Island, name=island)
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(island=island).order_by('weight')
    else:
        bookings = Booking.objects.filter(island=island, is_public=True).order_by('weight')
    page_obj, page_range = paginate_bookings(bookings, request)

    context = {
        'types' : filter_categories(island, request),
        'page_obj' : page_obj,
        'islands': Island.objects.all().order_by('modified'),
        'current_island':island,
        'current_category' : None,
        'breadcrumb' : 'All Bookings',
        'page_range': page_range,
        'jumbotron_path' : f"core/assets/{island}.jpg"
    }

    if page_obj.number == 1:
        context.update({'jumbotron':True})
    return render(request, 'core/base_site.html', context)


def log_cat_traffic(request, island, category):
    if request.user.is_anonymous:
        log_traffic(instance=get_object_or_404(Category, name=category))
    return redirect('core:view-by-cat', island, category)


def view_by_cat(request, island, category):
    island = get_object_or_404(Island, name=island)
    category = get_object_or_404(Category, name=category)
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(island=island, tags=category).order_by('weight')
    else:
        bookings = Booking.objects.filter(island=island, is_public=True, tags=category).order_by('weight')
    page_obj, page_range = paginate_bookings(bookings, request)

    context = {
        'types' : filter_categories(island, request),
        'page_obj' : page_obj,
        'islands':Island.objects.all().order_by('modified'),
        'current_island':island,
        'current_category': category,
        'breadcrumb' : category,
        'page_range': page_range,
        'jumbotron_path' : f"core/assets/{island}.jpg",
    }

    if page_obj.number == 1:
        context.update({'jumbotron':True})
    return render(request, 'core/base_site.html', context)


def view_by_type(request, island, type):
    island = get_object_or_404(Island, name=island)
    type = get_object_or_404(Type, name=type)
    categories = Category.objects.filter(type=type)

    if request.user.is_authenticated:
        bookings = Booking.objects.filter(island=island, tags__in=categories).distinct().order_by('weight')
    else:
        bookings = Booking.objects.filter(island=island, is_public=True, tags__in=categories).distinct().order_by('weight')
    page_obj, page_range = paginate_bookings(bookings, request)

    context = {
        'types' : filter_categories(island, request),
        'page_obj' : page_obj,
        'islands':Island.objects.all().order_by('modified'),
        'current_island':island,
        'current_category': None,
        'breadcrumb' : type,
        'page_range': page_range,
        'jumbotron_path' : f"core/assets/{island}.jpg",
    }

    if page_obj.number == 1:
        context.update({'jumbotron':True})
    return render(request, 'core/base_site.html', context)


def log_search(request, island):
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
        Q(tags__name__icontains=query), 
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
            Q(tags__name__icontains=query), 
            island=island,
        ).distinct().order_by('weight')
    else:
        bookings = Booking.objects.filter( 
            Q(title__icontains=query) | 
            Q(company_name__icontains=query) | 
            Q(city__icontains=query) | 
            Q(fh_id__icontains=query) | 
            Q(tags__name__icontains=query), 
            island=island,
            is_public=True,
        ).distinct().order_by('weight')
    page_obj, page_range = paginate_bookings(bookings, request)

    context = {
        'types' : filter_categories(island, request),
        'page_obj' : page_obj,
        'islands':Island.objects.all().order_by('modified'),
        'current_island':island,
        'current_category': None,
        'breadcrumb' : query,
        'page_range': page_range,
        'query':query,
    }
    return render(request, 'core/search.html', context)


def booking_update(request, pk):
    if request.method == 'GET':
        booking = get_object_or_404(Booking, pk=pk)

        context = {
            'booking' : booking,
            'categories': Category.objects.all().order_by('name'),
            'types' : Type.objects.all(),
            'current_island' : request.GET.get('island'),
            'page' : request.GET.get('page'),
            'current_category' : request.GET.get('category'),
        }
        return render(request, 'core/update.html', context)
    else:
        booking = get_object_or_404(Booking, pk=pk)
        booking.title = request.POST['title']
        booking.is_public = True if request.POST['is_public'] == 'true' else False
        booking.is_popular = True if request.POST['is_popular'] == 'true' else False
        booking.is_pinned = True if request.POST['is_pinned'] == 'true' else False
        booking.is_promo = True if request.POST['is_promo'] == 'true' else False
        booking.weight = request.POST['weight']
        booking.promo_amount = request.POST['promo_amount']
        booking.promo_code = request.POST['promo_code']
        booking.city = request.POST['city']
        
        if booking.is_public:
            booking.is_verified = True
        
        category_ids = request.POST.getlist('category_ids')
        if category_ids:
            tags = Category.objects.filter(pk__in=category_ids)
            booking.tags.set(tags)

        booking = update_booking_weight(booking)
        booking.save()
    
    island = request.GET.get('island')
    category = request.GET.get('category')
    page = request.GET.get('page')
    return redirect(reverse('core:booking-update', kwargs={'pk':booking.pk}) + f'?island={island}&category={category}&page={page}')


def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.delete()

    island=request.POST['current_island']
    page_number = request.POST['page']
    if request.POST['current_category'] == 'None':
        return redirect(reverse('core:change-island', kwargs={'island': island}) + f'?page={page_number}' + f'#{booking.fh_id}')
    category = request.POST['current_category']
    return redirect(reverse('core:category-results', kwargs={'island': island, 'category':category}) + f'?page={page_number}' + f'#{booking.fh_id}')


def contact_garett(request):
    return render(request, 'core/contact_garett.html')


def logout_admin(request, island):
    logout(request)
    return redirect('core:change-island', island=island)

