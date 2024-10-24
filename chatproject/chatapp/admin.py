from django.contrib import admin

from chatapp import models

# Register your models here.

admin.site.register(models.ChatThread)
admin.site.register(models.ChatHistory)
