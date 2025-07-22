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
    header_element = models.CharField(max_length=60, blank=True)

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
    title = models.CharField(max_length=50, blank=True)
    image_URL = models.URLField()
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
    city = models.CharField(max_length=100)
    tags = models.ManyToManyField('Category', related_name='bookings')
    island = models.ForeignKey(Island, on_delete=models.CASCADE)
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




