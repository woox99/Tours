from django.contrib import admin
from core.models import *

class BookingAdmin(admin.ModelAdmin):
    search_fields = ['title', 'fh_id']
    list_display = ['title', 'is_public',  'is_verified', 'company_name',  'fh_id', 'island', 'weight', 'is_promo', 'promo_amount']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'is_popular', 'traffic', 'public_bookings_count']

class IslandAdmin(admin.ModelAdmin):
    list_display = ['name', 'bookings']


class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'island', 'count', 'results', 'created']

class SiteVisitAdmin(admin.ModelAdmin):
    list_display = ['created', 'ref']



# Register your models here.
admin.site.register(Booking, BookingAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Island, IslandAdmin)
admin.site.register(SearchQuery, SearchQueryAdmin)
admin.site.register(SiteVisit, SiteVisitAdmin)
# admin.site.register(Type)
