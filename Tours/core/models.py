from django.db import models


# Create your models here.
class Quote(models.Model):
    hawaiian = models.CharField(max_length=100)
    english = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.hawaiian}"


class Type(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    is_popular = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Island(models.Model):
    name = models.CharField(max_length=50)

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

    def __str__(self):
        return self.title
    





