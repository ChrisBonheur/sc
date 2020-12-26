from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^new_message/', views.new_msg, name="new_msg"),
    re_path(r'^box_message/', views.box_msg, name="box_msg"),
    re_path(r'^notifications/', views.notifications, name="notifications"),
    re_path(r'^redirect-from-notif/', views.notif_detail, name="notif_redirect"),
]

app_name = "communication"