from django.db import models
from django.contrib.auth.models import User
from telegram_app.models import TelegramUser
# Create your models here.
class CustomUser(User):
    telegram_user = models.ForeignKey(TelegramUser, on_delete=models.SET_NULL, null=True, blank=True)