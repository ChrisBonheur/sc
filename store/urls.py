from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.home, name="home"),
    re_path(r'^(?P<article_id>[0-9]+)/$', views.detail, name='detail'),
    re_path(r'^poster-un-article/', views.create_article, name="create_article"),
    re_path(r'^modifier-article/(?P<article_id>[0-9]+)/$', views.update, name='update'),
    re_path(r'^mes-articles-favoris/$', views.favourite, name="favourite"),
    re_path(r'^search/', views.search, name="search"),
]

app_name = 'store'