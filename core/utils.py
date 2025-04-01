import random
from django.templatetags.static import static
from core.models import *
from django.utils.timezone import now 
from django.core.paginator import Paginator
from django.db.models import F


import time #debug


def log_traffic(instance):
    instance.traffic=F('traffic') + 1
    instance.save()
    return


def paginate_bookings(bookings, request, per_page=12):
    paginator = Paginator(bookings, per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(page_number, on_each_side=0, on_ends=1)
    return page_obj, page_range


def update_all_booking_weights(bookings):
    updated_bookings = []
    public_bookings_count = bookings.filter(is_public=True).count()
    top_percentile = round(public_bookings_count / 100)

    for booking in bookings:
        if not booking.is_pinned and not booking.is_popular and booking.is_verified:
            booking.weight = random.randint(1, public_bookings_count)
        booking.modified = now() # Must manually update modified during bulk_update()
        updated_bookings.append(booking)

    Booking.objects.bulk_update(updated_bookings, ['weight', 'modified'])
    return


def update_booking_weight(booking):
    public_bookings_count = Booking.objects.filter(is_public=True).count()
    # top_percentile = round(public_bookings_count / 100)
    # print(top_percentile)

    if booking.is_pinned:
        booking.weight = 0
    elif booking.is_popular:
        booking.weight = random.randint(1, 20)
    elif not booking.is_pinned and booking.weight == 0:
        booking.weight = random.randint(1, public_bookings_count)
    return booking


def get_tours(island, request):
    tours = []
    
    type = Type.objects.get(name='Tour')
    tour_set = Category.objects.filter(type=type).order_by('name')
    if request.user.is_authenticated:
        return tour_set
    for category in tour_set:
        if category.bookings.filter(island=island, is_public=True).exists():
            tours.append(category)
    return tours


def get_activities(island, request):
    activities = []
    other = None

    type = Type.objects.get(name='Activity')
    activity_set = Category.objects.filter(type=type).order_by('name')
    if request.user.is_authenticated:
        return activity_set
    for category in activity_set:
        if category.bookings.filter(island=island, is_public=True).exists():
            if category.name == 'Other':
                other = category
            else:
                activities.append(category)
    if other:
        activities.append(other)
    return activities


    #     # Import Fareharbor csv data script
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