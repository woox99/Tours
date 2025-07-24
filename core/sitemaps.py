from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Island, Category, Type

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        # Exclude core:index because it redirects permenantly
        return ['core:info', 'core:contact-garett']

    def location(self, item):
        return reverse(item)

class IslandSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        return Island.objects.all()

    def lastmod(self, obj):
        return obj.modified

    def location(self, obj):
        return reverse('core:change-island', args=[obj.name])

class CategoryByIslandSitemap(Sitemap):
    priority = 0.9
    changefreq = 'daily'

    def items(self):
        pairs = []
        islands = Island.objects.all()

        for island in islands:
            for type in Type.objects.all():
                valid_categories = [
                    cat for cat in type.category_set.all()
                    if cat.bookings.filter(island=island, is_public=True).exists()
                ]

                for category in valid_categories:
                    pairs.append((island, category))

        return pairs

    def location(self, obj):
        island, category = obj
        return reverse('core:change-cat', args=[island.name, category.name])
