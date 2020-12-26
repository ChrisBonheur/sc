from django.contrib import admin

from .models import Message, Talk

admin.site.register(Message)
admin.site.register(Talk)
