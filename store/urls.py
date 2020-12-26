from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.home, name="home"),
    re_path(r'^(?P<article_id>[0-9]+)/$', views.detail, name='detail'),
    re_path(r'^sell/', views.sell, name="sell"),
    re_path(r'^favourite/', views.favourite, name="favourite"),
    re_path(r'^search/', views.search, name="search"),
]

app_name = 'store'