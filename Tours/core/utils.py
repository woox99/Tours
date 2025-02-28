import random
from django.templatetags.static import static
from core.models import Quote

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
    }




    # # Import Fareharbor csv data script
    # path = 'core/fh.csv'
    # with open(path, newline='', encoding='utf-8') as csvfile:
    #     reader = csv.DictReader(csvfile)
    #     for row in reader:
    #         # print(reader.fieldnames)
    #         try:
    #             booking = Booking(
    #                 title=row["item_name"],
    #                 company_name=row["company_name"],
    #                 city=row["city"],
    #                 category=Category.objects.get(name=row["category"]),
    #                 type=Type.objects.get(name=row["item_type"]),
    #                 island=Island.objects.get(name=row["island"]),
    #                 fareharbor_item_id=int(row["item_id"]),
    #                 referral_link=row["referral_link"],
    #                 image_URL=row["image_URL"],
    #             )
    #             booking.save()
    #         except Exception as e:
    #             print(f"Skipping row due to error: {e}")

            # try:
            #     category = Category.objects.get(name=row["category"])
            # except Category.DoesNotExist:
            #     type = Type.objects.get(name=row["item_type"])
            #     category = Category.objects.create(name=row["category"], type=type)
            
            # try:
            #     island = Island.objects.get(name=row["island"])
            # except Island.DoesNotExist:
            #     island = Island.objects.create(name=row["island"])