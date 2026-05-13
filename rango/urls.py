from django.urls import path
from rango import views

app_name = 'rango'
name = 'about'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
]