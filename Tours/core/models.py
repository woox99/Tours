from django.db import models
from django.utils import timezone


# Create your models here.
class Quote(models.Model):
    hawaiian = models.CharField(max_length=100)
    english = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.hawaiian}"


class Type(models.Model):
    name = models.CharField(max_length=50, unique=True)
    clicks = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    is_popular = models.BooleanField(default=False)
    clicks = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Island(models.Model):
    name = models.CharField(max_length=50, unique=True)
    clicks = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Booking(models.Model):
    title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    island = models.ForeignKey(Island, on_delete=models.CASCADE)
    fareharbor_item_id = models.IntegerField()
    referral_link = models.URLField()
    image_URL = models.URLField()
    clicks = models.IntegerField(default=0)
    weight = models.IntegerField(default=2500)
    modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
    

class SiteVisit(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return timezone.localtime(self.created).strftime('%b %d, %I:%M %p')
    

class SearchQuery(models.Model):
    query = models.TextField()
    island = models.ForeignKey(Island, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    results = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'"{self.query}"'




