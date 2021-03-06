from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.my_articles, name='my_articles'),
    re_path(r'^update/(?P<article_id>[0-9]+)/$', views.update_article, name='update'),
    re_path(r'^delete/', views.delete_article, name='delete'),
    re_path(r'^selled_list/$', views.selled_article_list, name='selled_list'),
    re_path(r'^bought_list/$', views.bought_article_list, name='bought_list'),
    #ajout provisoire de url
    re_path(r'^factures/[a-z.ç]*', views.invoices, name="invoices"),
    re_path(r'^commandes/[a-zç]*$', views.orders, name="orders"),
]

app_name = 'dashboard'