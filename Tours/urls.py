from django.contrib import admin
from django.urls import path, include 

handler404 = 'core.views.error_404_view'

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('core.urls')), 
]