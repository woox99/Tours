from django.contrib import admin
from core.models import *

class BookingAdmin(admin.ModelAdmin):
    list_display = ['title', 'company_name', 'island', 'category', 'clicks']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'is_popular', 'clicks']

class IslandAdmin(admin.ModelAdmin):
    list_display = ['name', 'clicks']

class QuoteAdmin(admin.ModelAdmin):
    list_display = ['hawaiian', 'english']

class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'island', 'count', 'results', 'created']



# Register your models here.
admin.site.register(Booking, BookingAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Island, IslandAdmin)
admin.site.register(Quote, QuoteAdmin)
admin.site.register(SearchQuery, SearchQueryAdmin)
admin.site.register(SiteVisit)
# admin.site.register(Type)
