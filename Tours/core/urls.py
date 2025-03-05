from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:island>/', views.change_island, name='change-island'),
    path('<str:island>/search-log/', views.search_log, name='search'),
    path('<str:island>/search/', views.search_results, name='search-results'),
    path('<str:island>/<str:category>/', views.change_category, name='change-category'), # keep at bottom
]