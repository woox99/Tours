from django.contrib import admin
from core.models import *

class BookingAdmin(admin.ModelAdmin):
    search_fields = ['title', 'fh_id']
    list_display = ['title', 'is_public', 'company_name',  'fh_id', 'island', 'weight', 'is_promo', 'promo_amount']
    ordering = ['title']

class TypeAdmin(admin.ModelAdmin):
    ordering = ['modified']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'public_bookings', 'is_popular', 'traffic']
    ordering = ['name']

class IslandAdmin(admin.ModelAdmin):
    list_display = ['name', 'bookings', 'public_bookings']
    ordering = ['modified']

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
admin.site.register(Type, TypeAdmin)
