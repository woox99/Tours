from django.contrib import admin
from core.models import *

class BookingAdmin(admin.ModelAdmin):
    list_display = ['title', 'island', 'category']

# Register your models here.
admin.site.register(Booking, BookingAdmin)
admin.site.register(Quote)
admin.site.register(Type) # remove
admin.site.register(Island)
admin.site.register(Category)
