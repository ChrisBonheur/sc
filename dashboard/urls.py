from django.urls import re_path

from . import views

urlpatterns = [
    # re_path(r'^$', views.my_articles, name='my_articles'),
    # re_path(r'^delete/', views.delete_article, name='delete'),
    # re_path(r'^selled_list/$', views.selled_article_list, name='selled_list'),
    # re_path(r'^bought_list/$', views.bought_article_list, name='bought_list'),
    #ajout provisoire de url
    re_path(r'^factures/[a-z.ç]*', views.invoices, name="invoices"),
    re_path(r'^commandes/[a-zç]*$', views.orders, name="orders"),
    re_path(r'^payement/', views.payement, name="payement"),
    re_path(r'^achats-en-attentes/$', views.transactions, name="waiting-buy"),
    re_path(r'^ventes-en-attentes/$', views.transactions, name="waiting-sell"),
    re_path(r'^achats-effectués/$', views.transactions, name="articles-bought"),
    re_path(r'^ventes-réalisées/$', views.transactions, name="articles-selled"),
]

app_name = 'dashboard'