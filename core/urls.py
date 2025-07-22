from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('info/', views.info, name='info'),
    path('booking-update/<int:pk>/', views.booking_update, name='booking-update'),
    path('booking-delete/<int:pk>/', views.booking_delete, name='booking-delete'),
    path('contact-garett/', views.contact_garett, name='contact-garett'),
    path('<str:island>/', views.view_by_island, name='change-island'),
    path('<str:island>/search-log/', views.log_search, name='search'),
    path('<str:island>/search/', views.search_results, name='search-results'),
    path('<str:island>/logout/', views.logout_admin, name='logout'),
    path('<str:island>/<str:category>/log-cat-traffic/', views.log_cat_traffic, name='change-cat'),
    path('<str:island>/<str:category>/', views.view_by_cat, name='view-by-cat'), # keep at bottom
]