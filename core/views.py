from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required

from core.utils import *
from core.models import *

from urllib.parse import quote
from datetime import timedelta
import csv # debug
import time #debug


def home(request):
    # count = 0
    # for booking in Booking.objects.all():
    #     if 'filestackcontent.com/' in booking.image_URL and 'resize=width:500/' not in booking.image_URL:
    #         booking.image_URL = booking.image_URL.replace(
    #             'filestackcontent.com/',
    #             'filestackcontent.com/resize=width:500/'
    #         )
    #         # booking.save()
    #         count = count + 1
    #         print(count)
    #     print(booking.image_URL)

    # for booking in Booking.objects.all():
    #     if '&back=BACKLINK' in booking.referral_link:
    #         booking.referral_link = booking.referral_link.replace(
    #             '&back=BACKLINK',
    #             ''
    #         )
    #         # booking.save()
    #         count = count + 1
    #         print(count)
    #     print(booking.referral_link)

    if 'island' in request.session:
        try:
            island = Island.objects.get(name=request.session['island'])
        except Island.DoesNotExist:
            island = Island.objects.all().order_by('modified').first()
    else:
        island = Island.objects.all().order_by('modified').first()

    context = {
        'types' : filter_categories(island, request),
        'islands': Island.objects.all().order_by('modified'),
        'current_island': island,
        'current_category' : None,
    }
    return render(request, 'core/home_redirect.html',  context)


# def home(request):
#     if 'island' in request.session:
#         try:
#             island = Island.objects.get(name=request.session['island'])
#         except Island.DoesNotExist:
#             island = Island.objects.all().order_by('modified').first()
#     return render(request, 'core/home_redirect.html', {'island': island})


def view_by_island(request, island):
    # Randomize booking weights periodically
    last_weight_randomization = BookingRandomization.objects.last()
    if not last_weight_randomization:
        last_weight_randomization = BookingRandomization.objects.create()
    last_weight_randomization_date = last_weight_randomization.date
    if now() - last_weight_randomization_date > timedelta(days=1):
        randomize_booking_weights()

    island = get_object_or_404(Island, name=island)
    request.session['island'] = island.name
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(island=island).order_by('weight')
    else:
        bookings = Booking.objects.filter(island=island, is_public=True).order_by('weight')
    page_obj, page_range = paginate_bookings(bookings, request)

    back_url = f'www.hawaiitraveltips.com/{quote(island.name)}/?page={page_obj.number}'

    context = {
        'types' : filter_categories(island, request),
        'page_obj' : page_obj,
        'islands': Island.objects.all().order_by('modified'),
        'current_island': island,
        'current_category' : None,
        'breadcrumb' : 'All Bookings',
        'page_range': page_range,
        'back_url': quote(back_url),
    }

    if page_obj.number == 1:
        context.update({'jumbotron':True})
    return render(request, 'core/base_site.html', context)


def info(request):
    return render(request, 'core/info.html')


def error_404_view(request, exception):
    islands = Island.objects.all().order_by('modified')
    return render(request, 'core/404.html', {'islands':islands}, status=404)


# Log the traffic each time a category is selected
# def log_cat_traffic(request, island, category):
#     if request.user.is_anonymous:
#         log_traffic(category)
#     return redirect('core:view-by-cat', island, category)


def view_by_cat(request, island, category):
    island = get_object_or_404(Island, name=island)
    category = get_object_or_404(Category, name=category)
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(island=island, tags=category).order_by('weight')
    else:
        bookings = Booking.objects.filter(island=island, is_public=True, tags=category).order_by('weight')
    page_obj, page_range = paginate_bookings(bookings, request)

    back_url = f'www.hawaiitraveltips.com/{quote(island.name)}/{quote(category.name)}/?page={page_obj.number}'

    context = {
        'types' : filter_categories(island, request),
        'page_obj' : page_obj,
        'islands':Island.objects.all().order_by('modified'),
        'current_island': island,
        'current_category': category,
        'breadcrumb' : category,
        'page_range': page_range,
        'back_url': quote(back_url),
    }

    if page_obj.number == 1:
        context.update({'jumbotron':True})
    return render(request, 'core/base_site.html', context)


# Log the query and count of results for each search
def log_search(request, island):
    island = get_object_or_404(Island, name=island)
    query = request.GET.get('q', '')

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
    # Get results count
    results = get_search_results(request, island, query).count()
    new_search_query.results = results
    new_search_query.save()

    return redirect(reverse('core:search-results', kwargs={'island': island.name}) + f'?q={query}')


def search_results(request, island):
    island = get_object_or_404(Island, name=island)
    query = request.GET.get('q', '')
    bookings = get_search_results(request, island, query)
    page_obj, page_range = paginate_bookings(bookings, request)

    back_url = f'www.hawaiitraveltips.com/{quote(island.name)}/search/?page={page_obj.number}&q={quote(query)}'

    context = {
        'types' : filter_categories(island, request),
        'page_obj' : page_obj,
        'islands':Island.objects.all().order_by('modified'),
        'current_island': island,
        'current_category': None,
        'breadcrumb' : query,
        'page_range': page_range,
        'query':query,
        'back_url': quote(back_url),
    }
    return render(request, 'core/search.html', context)


@staff_member_required
def booking_update(request, pk):
    if request.method == 'GET':
        booking = get_object_or_404(Booking, pk=pk)
        context = {
            'islands':Island.objects.all().order_by('modified'),
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
        update_booking(request, booking)
    
    island = request.GET.get('island')
    category = request.GET.get('category')
    page = request.GET.get('page')
    return redirect(reverse('core:booking-update', kwargs={'pk':booking.pk}) + f'?island={island}&category={quote(category)}&page={page}')


@staff_member_required
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.delete()

    island=request.POST['current_island']
    page_number = request.POST['page']
    if request.POST['current_category'] == 'None':
        return redirect(reverse('core:change-island', kwargs={'island': island}) + f'?page={page_number}' + f'#{booking.fh_id}')
    category = request.POST['current_category']
    return redirect(reverse('core:view-by-cat', kwargs={'island': island, 'category':category}) + f'?page={page_number}' + f'#{booking.fh_id}')


def contact_garett(request):
    return render(request, 'core/contact_garett.html')


def logout_admin(request, island):
    logout(request)
    return redirect('core:change-island', island=island)



# def view_by_type(request, island, type):
#     island = get_object_or_404(Island, name=island)
#     type = get_object_or_404(Type, name=type)
#     categories = Category.objects.filter(type=type)

#     if request.user.is_authenticated:
#         bookings = Booking.objects.filter(island=island, tags__in=categories).distinct().order_by('weight')
#     else:
#         bookings = Booking.objects.filter(island=island, is_public=True, tags__in=categories).distinct().order_by('weight')
#     page_obj, page_range = paginate_bookings(bookings, request)

#     back_url = f'www.hawaiitraveltips.com/{quote(island.name)}/all-{quote(type.name)}/?page={page_obj.number}'

#     context = {
#         'types' : filter_categories(island, request),
#         'page_obj' : page_obj,
#         'islands':Island.objects.all().order_by('modified'),
#         'current_island': island,
#         'current_category': None,
#         'breadcrumb' : type,
#         'page_range': page_range,
#         'back_url': quote(back_url),
#     }

#     if page_obj.number == 1:
#         context.update({'jumbotron':True})
#     return render(request, 'core/base_site.html', context)

