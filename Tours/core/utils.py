import random
from django.templatetags.static import static
from core.models import *
from django.utils.timezone import now 
from datetime import timedelta 
from django.db.models import F


def get_collage():
    asset_ids = []
    top_row_collage_urls = []
    bottom_row_collage_urls = []

    for i in range(0, 14, 1):
        num = random.randint(1,31)
        while num in asset_ids:
            num = random.randint(1,31)
        asset_ids.append(num)
    for i in asset_ids:
        url = static(f'core/collage/{i}.jpg')
        if len(top_row_collage_urls) < 8:
            top_row_collage_urls.append(url)
        else:
            bottom_row_collage_urls.append(url)
        
    return {
        'top_row_urls' : top_row_collage_urls,
        'bottom_row_urls' : bottom_row_collage_urls,
        'quote': Quote.objects.order_by('?').first(),
        'collage' : True,
    }


# Randomizes bookings weights if booking hasn't been clicked in days=1
def randomize_booking_weights():
    bookings = Booking.objects.filter(modified__lt=now() - timedelta(days=1))

    updated_bookings = []
    total_bookings = bookings.count()

    for booking in bookings:
        booking.weight = random.randint(0, total_bookings)
        booking.modified = now()
        updated_bookings.append(booking)

    Booking.objects.bulk_update(updated_bookings, ['weight', 'modified'])
    return


def get_tours(island):
    tours = []
    type = Type.objects.filter(name='Tour').first()

    tour_set = Category.objects.filter(type=type).order_by('name')
    for category in tour_set:
        if len(category.booking_set.filter(island=island)):
            tours.append(category)
    return tours


def get_activities(island):
    activities = []
    type = Type.objects.filter(name='Activity').first()

    activity_set = Category.objects.filter(type=type).exclude(name='Other').order_by('name')
    for category in activity_set:
        if len(category.booking_set.filter(island=island)):
            activities.append(category)
    return activities


def increase_instance_clicks(instance):
    instance.clicks = F('clicks') + 1
    instance.save()
    return


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