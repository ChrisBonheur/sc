from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.my_articles, name='my_articles'),
    re_path(r'^update/(?P<article_id>[0-9]+)/$', views.update_article, name='update'),
    re_path(r'^delete/', views.delete_article, name='delete'),
    re_path(r'^sent_order/$', views.sent_order, name="sent_order"),
    re_path(r'^received_order/$', views.received_order, name="received_order"),
    re_path(r'^delete_order/(?P<order_id>[0-9]+)/$', views.delete_order, name="delete_order"),
    re_path(r'^create_order/(?P<article_id>[0-9]+)/$', views.create_order, name="create_order"),
    re_path(r'^create_invoice/', views.create_invoice, name="create_invoice"),
    re_path(r'^received_invoice/', views.received_invoice, name="received_invoice"),
    re_path(r'^delete_invoice/(?P<invoice_id>[0-9]+)/$', views.delete_invoice, name="delete_invoice"),
    re_path(r'^selled_list/$', views.selled_article_list, name='selled_list'),
    re_path(r'^bought_list/$', views.bought_article_list, name='bought_list'),
]

app_name = 'dashboard'