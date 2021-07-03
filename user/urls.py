from django.urls import re_path

from user import views

urlpatterns = [
    re_path(r'^login/', views.login_user, name="login"),
    re_path(r'^register/', views.register, name="register"),
    re_path(r'^auto_login/', views.auto_login, name="auto_login"),
    re_path(r'^profil/', views.profil, name="profil"),
    re_path(r'^security/', views.security, name="security"),
    re_path(r'^logout/', views.logout_user, name='logout'),
]

app_name = 'user'