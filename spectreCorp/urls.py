"""spectreCorp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path, re_path
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from store import views 

urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    re_path('^store/', include('store.urls')),
    path('admin/', admin.site.urls),
    re_path(r'^message/', include('communication.urls')),
    re_path(r'^user/', include('user.urls')),
    re_path(r'dashboard/', include('dashboard.urls')),
    path('accounts/', include('allauth.urls')),
    url('', include('pwa.urls')),
    re_path('^no_connection/$', TemplateView.as_view(template_name='no_connection.html')),
    path('about/', TemplateView.as_view(template_name='about.html'), name="about"),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name="contact"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         re_path('^__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns
