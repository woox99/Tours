from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('booking-update/<int:pk>/', views.booking_update, name='booking-update'),
    path('booking-delete/<int:pk>/', views.booking_delete, name='booking-delete'),
    path('contact-garett/', views.contact_garett, name='contact-garett'),
    path('<str:island>/', views.change_island, name='change-island'),
    path('<str:island>/search-log/', views.search_log, name='search'),
    path('<str:island>/search/', views.search_results, name='search-results'),
    # path('<str:island>/tours/', views.tours, name='tours'),
    # path('<str:island>/activities/', views.activities, name='activities'),
    path('<str:island>/logout/', views.logout_admin, name='logout'),
    path('<str:island>/<str:category>/change-category/', views.change_category, name='change-category'),
    path('<str:island>/<str:category>/', views.category_results, name='category-results'), # keep at bottom
]