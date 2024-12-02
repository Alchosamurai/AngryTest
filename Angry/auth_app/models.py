from django.db import models
from django.contrib.auth.models import AbstractUser
from telegram_app.models import TelegramUser
# Create your models here.
class CustomUser(AbstractUser):
    telegram_user = models.ForeignKey(TelegramUser, on_delete=models.SET_NULL, null=True, blank=True)