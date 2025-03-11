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


def paginate_bookings(bookings, request, per_page=6):
    paginator = Paginator(bookings, per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(page_number, on_each_side=0, on_ends=1)
    return page_obj, page_range


def get_collage():
    collage_img_ids = random.sample(range(1, 32), 14)
    urls = [static(f'core/collage/{i}.jpg') for i in collage_img_ids]

    return {
        'top_row_urls' : urls[:8],
        'bottom_row_urls': urls[8:],
        'quote': Quote.objects.order_by('?').first(),
        'collage' : True,
    }


def randomize_booking_weights(bookings):
    updated_bookings = []
    total_bookings = bookings.count()

    for booking in bookings:
        booking.weight = random.randint(0, total_bookings)
        booking.modified = now() # Must manually update modified during bulk_update()
        updated_bookings.append(booking)

    Booking.objects.bulk_update(updated_bookings, ['weight', 'modified'])
    return


def get_tours(island):
    tours = []
    
    type = Type.objects.get(name='Tour')
    tour_set = Category.objects.filter(type=type).order_by('name')

    for category in tour_set:
        if category.booking_set.filter(island=island).exists():
            tours.append(category)
    return tours


def get_activities(island):
    activities = []
    other = None

    type = Type.objects.get(name='Activity')
    activity_set = Category.objects.filter(type=type).order_by('name')
    
    for category in activity_set:
        if category.booking_set.filter(island=island).exists():
            if category.name == 'Other':
                other = category
            else:
                activities.append(category)
    if other:
        activities.append(other)
    return activities


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
    #                 category=category,
    #                 # type=Type.objects.get(name=row["item_type"]),
    #                 island=island,
    #                 fareharbor_item_id=int(row["item_id"]),
    #                 referral_link=row["referral_link"],
    #                 image_URL=row["image_URL"],
    #             )
    #             booking.save()
    #         except Exception as e:
    #             print(f"Skipping row due to error: {e}")