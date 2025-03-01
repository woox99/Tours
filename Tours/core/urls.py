from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:island>/', views.change_island, name='change-island'),
]