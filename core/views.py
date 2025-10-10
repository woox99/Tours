from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required

import requests
from django.shortcuts import render

from core.utils import *
from core.models import *

from urllib.parse import quote
from datetime import timedelta
import csv # debug
import time #debug


def index(request):
    return redirect('core:home', permanent=True)

def home(request):
    if 'island' in request.session:
        try:
            island = Island.objects.get(name=request.session['island'])
        except Island.DoesNotExist:
            island = Island.objects.all().order_by('modified').first()
    else:
        island = Island.objects.all().order_by('modified').first()
    print(island.name)
    return redirect(f'/{island.name}/')


def view_island(request, island):

    # Randomize booking weights periodically
    last_weight_randomization = BookingRandomization.objects.last()
    if not last_weight_randomization:
        last_weight_randomization = BookingRandomization.objects.create()
    last_weight_randomization_date = last_weight_randomization.date
    if now() - last_weight_randomization_date > timedelta(days=3):
        randomize_booking_weights()

    island = get_object_or_404(Island, name=island)
    request.session['island'] = island.name

    # WordPress.com REST API endpoint - Limit = 3
    WP_API_URL = "https://public-api.wordpress.com/wp/v2/sites/team92d3a5e49bc-kctlm.wordpress.com/posts?per_page=3"

    try:
        response = requests.get(WP_API_URL, timeout=5)
        response.raise_for_status()
        wp_posts = response.json()
    except requests.exceptions.RequestException as e:
        print("Error fetching WordPress posts:", e)
        wp_posts = []

    if request.user.is_authenticated:
        bookings = Booking.objects.filter(island=island).order_by('weight')[:3]
    else:
        bookings = Booking.objects.filter(island=island, is_public=True).order_by('weight')[:3]
    page_obj, page_range = paginate_bookings(bookings, request)

    back_url = f'www.hawaiitraveltips.com/{quote(island.name)}/?page={page_obj.number}'

    context = {
        'types' : filter_categories(island, request),
        'popular_categories' : Category.objects.filter(is_popular=True),
        'page_obj' : page_obj,
        'islands': Island.objects.all().order_by('modified'),
        'current_island': island,
        'current_category' : None,
        'breadcrumb' : 'All Bookings',
        'page_range': page_range,
        'back_url': quote(back_url),
        'bookings' : bookings,
        'wp_posts' : wp_posts,

    }
    return render(request, 'core/views/island.html', context)


def view_bookings(request, island):
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
        'popular_categories' : Category.objects.filter(is_popular=True),
        'page_obj' : page_obj,
        'islands': Island.objects.all().order_by('modified'),
        'current_island': island,
        'current_category' : None,
        'breadcrumb' : 'All Bookings',
        'page_range': page_range,
        'back_url': quote(back_url),
        'bookings' : bookings,

    }

    if page_obj.number == 1:
        context.update({'jumbotron':True})
    return render(request, 'core/views/booking_list.html', context)


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
        'bookings' : bookings,
    }

    if page_obj.number == 1:
        context.update({'jumbotron':True})
    return render(request, 'core/views/booking_list.html', context)

def post_list(request, island):
    island = get_object_or_404(Island, name=island)
    request.session['island'] = island.name

    # WordPress.com REST API endpoint
    WP_API_URL = "https://public-api.wordpress.com/wp/v2/sites/team92d3a5e49bc-kctlm.wordpress.com/posts"

    try:
        response = requests.get(WP_API_URL, timeout=5)
        response.raise_for_status()
        wp_posts = response.json()
    except requests.exceptions.RequestException as e:
        print("Error fetching WordPress posts:", e)
        wp_posts = []

    bookings = Booking.objects.filter(island=island, is_public=True).order_by('weight')[:3]
    page_obj, page_range = paginate_bookings(bookings, request)

    back_url = f'www.hawaiitraveltips.com/{quote(island.name)}/?page={page_obj.number}'

    context = {
        'types' : filter_categories(island, request),
        'popular_categories' : Category.objects.filter(is_popular=True),
        'page_obj' : page_obj,
        'islands': Island.objects.all().order_by('modified'),
        'current_island': island,
        'current_category' : None,
        'breadcrumb' : 'All Bookings',
        'page_range': page_range,
        'back_url': quote(back_url),
        'bookings' : bookings,
        'wp_posts' : wp_posts,

    }
    return render(request, 'core/views/post_list.html', context)

def post_detail(request, island, post_slug):
    island = get_object_or_404(Island, name=island)
    request.session['island'] = island.name

    # WordPress.com REST API endpoint
    WP_API_URL = f"https://public-api.wordpress.com/wp/v2/sites/team92d3a5e49bc-kctlm.wordpress.com/posts?slug={post_slug}"

    try:
        response = requests.get(WP_API_URL, timeout=5)
        response.raise_for_status()
        wp_data = response.json()
        wp_post = wp_data[0] if wp_data else None
    except requests.exceptions.RequestException as e:
        print("Error fetching WordPress post:", e)
        wp_post = None

    bookings = Booking.objects.filter(island=island, is_public=True).order_by('weight')[:3]
    page_obj, page_range = paginate_bookings(bookings, request)

    back_url = f'www.hawaiitraveltips.com/{quote(island.name)}/?page={page_obj.number}'

    context = {
        'types' : filter_categories(island, request),
        'popular_categories' : Category.objects.filter(is_popular=True),
        'page_obj' : page_obj,
        'islands': Island.objects.all().order_by('modified'),
        'current_island': island,
        'current_category' : None,
        'breadcrumb' : 'All Bookings',
        'page_range': page_range,
        'back_url': quote(back_url),
        'bookings' : bookings,
        'wp_post' : wp_post,

    }
    return render(request, 'core/views/post_detail.html', context)


def info(request):
    context = {
        'islands': Island.objects.all().order_by('modified'),
    }
    return render(request, 'core/views/info.html', context)


def error_404_view(request, exception):
    islands = Island.objects.all().order_by('modified')
    return render(request, 'core/views/404.html', {'islands':islands}, status=404)


# # Log the query and count of results for each search
# def log_search(request, island):
#     island = get_object_or_404(Island, name=island)
#     query = request.GET.get('q', '')

#     if request.user.is_authenticated:
#         return redirect(reverse('core:search-results', kwargs={'island': island.name}) + f'?q={query}')
    
#     search_queries = SearchQuery.objects.filter(query=query, island=island)

#     if search_queries.exists():
#         query_count = search_queries.count() + 1
#         search_queries.update(count=query_count)
#     else:
#         query_count = 1

#     # Save new query
#     new_search_query = SearchQuery.objects.create(
#         query=query, 
#         island=island,
#         count=query_count, 
#     )
#     # Get results count
#     results = get_search_results(request, island, query).count()
#     new_search_query.results = results
#     new_search_query.save()

#     return redirect(reverse('core:search-results', kwargs={'island': island.name}) + f'?q={query}')


# def search_results(request, island):
#     island = get_object_or_404(Island, name=island)
#     query = request.GET.get('q', '')
#     bookings = get_search_results(request, island, query)
#     page_obj, page_range = paginate_bookings(bookings, request)

#     back_url = f'www.hawaiitraveltips.com/{quote(island.name)}/search/?page={page_obj.number}&q={quote(query)}'

#     context = {
#         'types' : filter_categories(island, request),
#         'page_obj' : page_obj,
#         'islands':Island.objects.all().order_by('modified'),
#         'current_island': island,
#         'current_category': None,
#         'breadcrumb' : query,
#         'page_range': page_range,
#         'query':query,
#         'back_url': quote(back_url),
#     }
#     return render(request, 'core/search.html', context)


@staff_member_required
def booking_update(request, pk):
    island = request.GET.get('island')
    category = request.GET.get('category')
    page = request.GET.get('page')
    back_url = f'www.hawaiitraveltips.com/{quote(island)}/'

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
            'back_url': quote(back_url),

        }
        return render(request, 'core/views/update.html', context)
    else:
        booking = get_object_or_404(Booking, pk=pk)
        update_booking(request, booking)
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

