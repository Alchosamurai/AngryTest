from django.db import models
from uuid import uuid4

# Create your models here.
class TelegramUser(models.Model):
    chat_id = models.IntegerField()
    username = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return self.username if self.username else f"User {self.chat_id}"