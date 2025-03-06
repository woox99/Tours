import random
from django.templatetags.static import static
from core.models import *
from django.utils.timezone import now 
from django.core.paginator import Paginator


def paginate_bookings(bookings, request, per_page=6):
    paginator = Paginator(bookings, per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(page_number, on_each_side=0, on_ends=1)
    return page_obj, page_range

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
def randomize_booking_weights(bookings):

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
    
    type = Type.objects.get(name='Tour')
    tour_set = Category.objects.filter(type=type).order_by('name')

    for category in tour_set:
        if len(category.booking_set.filter(island=island)):
            tours.append(category)
    return tours


def get_activities(island):
    activities = []

    type = Type.objects.get(name='Activity')
    activity_set = Category.objects.filter(type=type).order_by('name')
    
    for category in activity_set:
        if len(category.booking_set.filter(island=island)):
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