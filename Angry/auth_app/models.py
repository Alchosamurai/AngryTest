from django.db import models
from django.contrib.auth.models import AbstractUser
from telegram_app.models import TelegramUser
from api.shemas import TelegramShema
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.db import transaction
from django.core.cache import cache
from uuid import uuid4

class CustomUser(AbstractUser):
    telegram_user = models.ForeignKey(TelegramUser, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)

    def generate_token_to_cache(self):
        token = str(uuid4())
        cache.set(token, self.id, 60 * 60 * 24)
        cache.set(f"user_{self.id}", token, 60 * 60 * 24)
        return token
    
    def check_token(self, token):
        return cache.get(f"user_{self.id}") == token
    
    def add_telegram_to_user(self, shema: TelegramShema.MergeTelegram):
        try:
            if TelegramUser.objects.filter(chat_id=shema.telegram_id).exists():
                telegram_user = TelegramUser.objects.filter(chat_id=shema.telegram_id).update(
                    username=shema.username,
                    full_name=shema.full_name
                )
                return True
            with transaction.atomic():
                telegram_user = TelegramUser.objects.create(
                    chat_id=shema.telegram_id,
                    username=shema.username,
                    full_name=shema.full_name
                )
                self.telegram_user = telegram_user
                self.save()
                return True
        except Exception as e:
            print(e)
            return False
    
    def add_phone_to_user(self, shema: TelegramShema.MergePhone):
        self.phone = shema.phone
        self.save()
    
    

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

@receiver(user_logged_in)
def user_logged_in_handler(request, user: CustomUser, **kwargs):
    user.generate_token_to_cache()
    print(f'Пользователь {user.username} вошел в систему.')
