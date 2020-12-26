from django.contrib import admin

from .models import Article, Category, Picture, Profil, Favourite
# Register your models here.

admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Picture)
admin.site.register(Profil)
admin.site.register(Favourite)
