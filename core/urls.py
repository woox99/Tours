from django.urls import path
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from . import views

app_name = 'core'

urlpatterns = [
    path("robots.txt", TemplateView.as_view(template_name="core/robots.txt", content_type="text/plain")),
    path('robots.txt/', RedirectView.as_view(url='/robots.txt', permanent=True)),
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('info/', views.info, name='info'),
    path('booking-update/<int:pk>/', views.booking_update, name='booking-update'),
    path('booking-delete/<int:pk>/', views.booking_delete, name='booking-delete'),
    path('contact-garett/', views.contact_garett, name='contact-garett'),
    path('test-site/', views.test_site, name='test-site'),
    path('<str:island>/top-activities/', views.view_activities, name='activities'),
    path('<str:island>/', views.view_by_island, name='change-island'),
    path('<str:island>/search-log/', views.log_search, name='search'),
    path('<str:island>/search/', views.search_results, name='search-results'),
    path('<str:island>/logout/', views.logout_admin, name='logout'),
    path('<str:island>/<str:category>/', views.view_by_cat, name='change-cat'), # keep at bottom
]