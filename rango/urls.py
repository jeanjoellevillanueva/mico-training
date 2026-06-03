from django.urls import path, include
from rango import views

app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('category/<slug:category_name_slug>/',
         views.show_category, name='show_category'),
    path('add_category/', views.add_category, name='add_category'),
    path('category/<slug:category_name_slug>/add_page/',
         views.add_page, name='add_page'),
    #path('login/', views.user_login, name='login'), # New Mapping for the login view
    path('register/', views.register, name='register'),
    path('restricted/', views.restricted, name='restricted'), # New Mapping for the restricted view
    #path('logout/', views.user_logout, name='logout'), # New Mapping for the logout view
    path('add_page/', views.add_page, name='add_page'),
    path('search/', views.search, name='search'),
    path('goto/', views.track_url, name='goto'),
]