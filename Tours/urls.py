from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import StaticViewSitemap, IslandSitemap, CategoryByIslandSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'islands': IslandSitemap,
    'categories': CategoryByIslandSitemap,
}

handler404 = 'core.views.error_404_view'

urlpatterns = [
    path("admin/", admin.site.urls),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', include('core.urls')),
]