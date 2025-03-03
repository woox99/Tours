from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('<str:island>/search', views.search, name='search'),
    path('<str:island>/', views.change_island, name='change-island'),
    path('<str:island>/<str:category>/', views.change_category, name='change-category'),
]