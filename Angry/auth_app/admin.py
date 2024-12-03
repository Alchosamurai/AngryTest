from django.contrib import admin
from .models import TelegramUser, CustomUser
# Register your models here.
admin.site.register(TelegramUser)
admin.site.register(CustomUser)