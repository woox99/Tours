import random
from django.templatetags.static import static
from core.models import *
from django.utils.timezone import now 
from django.core.paginator import Paginator
from django.db.models import F, Q
from django.shortcuts import get_object_or_404


# Update category traffic atomically
def log_traffic(category):
    Category.objects.filter(name=category).update(traffic=F('traffic') + 1)
    return


def paginate_bookings(bookings, request, per_page=6):
    paginator = Paginator(bookings, per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(page_number, on_each_side=0, on_ends=1)
    return page_obj, page_range


def randomize_booking_weights():
    updated_bookings = []
    bookings = Booking.objects.filter(is_public=True, is_pinned=False)
    public_bookings_count = bookings.count()
    if public_bookings_count < 20:
        public_bookings_count = 20

    for booking in bookings:
        if booking.is_popular:
            random.randint(1, 20)
        else:
            booking.weight = random.randint(1, public_bookings_count)
        booking.modified = now() # Must manually update modified during bulk_update()
        updated_bookings.append(booking)

    Booking.objects.bulk_update(updated_bookings, ['weight', 'modified'])
    BookingRandomization.objects.create()
    return


def update_booking_weight(booking):
    public_bookings_count = Booking.objects.filter(is_public=True).count()
    if public_bookings_count < 20:
        public_bookings_count = 20

    if booking.is_pinned:
        booking.weight = 0
    elif not booking.is_public:
        booking.weight = 10000
    elif booking.is_public and int(booking.weight) == 10000:
        booking.weight = random.randint(1, public_bookings_count)
    elif booking.is_popular and int(booking.weight) > 20:
        booking.weight = random.randint(1, 20)
    elif not booking.is_pinned and int(booking.weight) == 0:
        booking.weight = random.randint(1, public_bookings_count)
    return booking


def filter_categories(island, request):
    types = Type.objects.all().order_by('modified')
    if request.user.is_authenticated:
        for type in types:
            type.filtered_categories = sorted(
                [
                    cat for cat in type.category_set.all()
                    if cat.bookings.filter(island=island).exists()
                ],
                key=lambda cat: cat.name.lower()
            )
    else:
        for type in types:
            type.filtered_categories = sorted(
                [
                    cat for cat in type.category_set.all()
                    if cat.bookings.filter(island=island, is_public=True).exists()
                ],
                key=lambda cat: cat.name.lower()
            )
    return types


def update_booking(request, booking):
    booking.title = request.POST['title']
    booking.is_public = True if request.POST['is_public'] == 'true' else False
    booking.is_popular = True if request.POST['is_popular'] == 'true' else False
    booking.is_pinned = True if request.POST['is_pinned'] == 'true' else False
    booking.details = request.POST['details']
    booking.is_promo = True if request.POST['is_promo'] == 'true' else False
    booking.promo_amount = request.POST['promo_amount']
    booking.promo_code = request.POST['promo_code']
    booking.city = request.POST['city']
    booking.island = get_object_or_404(Island, pk=request.POST['island_id'])

    category_ids = request.POST.getlist('category_ids')
    if category_ids:
        tags = Category.objects.filter(pk__in=category_ids)
        booking.tags.set(tags)

    booking = update_booking_weight(booking)
    # booking.save()
    print(booking.island)
    return


def get_search_results(request, island, query):
    if request.user.is_authenticated:
        results = Booking.objects.filter( 
            Q(title__icontains=query) | 
            Q(company_name__icontains=query) | 
            Q(city__icontains=query) | 
            Q(fh_id__icontains=query) | 
            Q(tags__name__icontains=query), 
            island=island,
        ).distinct().order_by('weight')
    else:
        results = Booking.objects.filter( 
            Q(title__icontains=query) | 
            Q(company_name__icontains=query) | 
            Q(city__icontains=query) | 
            Q(fh_id__icontains=query) | 
            Q(tags__name__icontains=query), 
            island=island,
            is_public=True,
        ).distinct().order_by('weight')
    return results

    #  # change booking image URL
    # for booking in Booking.objects.all():
    #     # if 'filestackcontent.com/' in booking.image_URL and 'resize=width:500/' not in booking.image_URL:
    #     if 'filestackcontent.com/' in booking.image_URL:
    #         booking.image_URL = booking.image_URL.replace(
    #             'filestackcontent.com/',
    #             'filestackcontent.com/resize=width:720,fit:max/',
    #         )
    #         # booking.save()
    #     print(booking.image_URL)



    # # Import Fareharbor csv data script
    # path = 'core/fh.csv'
    # # with open(path, newline='', encoding='utf-8') as csvfile:
    # with open(path, newline='', encoding='utf-8-sig') as csvfile:
    #     reader = csv.DictReader(csvfile)
    #     for row in reader:
    #         # print(row)
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