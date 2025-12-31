from django.db import models
from django.utils import timezone



class Type(models.Model):
    name = models.CharField(max_length=50, unique=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    is_popular = models.BooleanField(default=False)
    traffic = models.IntegerField(default=0)
    page_title = models.CharField(max_length=80, default='Page Title')
    page_description = models.TextField(default='Page Description')

    @property
    def total_bookings(self):
        return self.bookings.count()

    @property
    def public_bookings(self):
        return self.bookings.filter(is_public=True).count()

    def __str__(self):
        return self.name


class Island(models.Model):
    name = models.CharField(max_length=50, unique=True)
    name_title = models.CharField(max_length=50, blank=True)
    wp_category_id = models.IntegerField(null=True, blank=True)
    hero_URL = models.URLField()
    hero_mobile_URL = models.URLField()
    island_page_title = models.CharField(max_length=80, default='Page Title')
    island_page_description = models.TextField(default='Page Description')
    bookings_page_title = models.CharField(max_length=80, default='Page Title')
    bookings_page_description = models.TextField(default='Page Description')
    # sm_featured_URL = models.URLField(blank=True)
    # sm_featured_company = models.CharField(max_length=50, blank=True)
    # lg_featured_URL = models.URLField(blank=True)
    # lg_featured_company = models.CharField(max_length=50, blank=True)

    modified = models.DateTimeField(auto_now=True)

    @property
    def total_bookings(self):
        return self.booking_set.all().count()
    
    @property
    def public_bookings(self):
        return self.booking_set.filter(is_public=True).count()

    def __str__(self):
        return self.name


class Booking(models.Model):
    title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100, blank=True)
    company_rating = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    company_reviews = models.IntegerField(max_length=5, blank=True, null=True)
    city = models.CharField(max_length=100)
    tags = models.ManyToManyField('Category', related_name='bookings')
    island = models.ForeignKey(Island, on_delete=models.CASCADE)
    details = models.TextField(blank=True)
    duration = models.CharField(max_length=10, blank=True)
    price = models.CharField(max_length=10, blank=True)
    is_public = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    is_promo = models.BooleanField(default=False)
    promo_amount = models.CharField(max_length=100, blank=True)
    promo_code = models.CharField(max_length=100, blank=True)
    fh_id = models.IntegerField(blank=True, null=True)
    referral_link = models.URLField()
    image_URL = models.URLField()
    weight = models.IntegerField(default=10000)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class SiteVisit(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    ref = models.CharField(max_length=100, default=None)
    
    def __str__(self):
        return timezone.localtime(self.created).strftime('%b %d, %I:%M %p')
    

class SearchQuery(models.Model):
    query = models.TextField()
    island = models.ForeignKey(Island, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    results = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'"{self.query}"'
    

class BookingRandomization(models.Model):
    date = models.DateTimeField(auto_now_add=True)




