from auth_app.models import CustomUser
from api.shemas import TelegramShema
from django.core.cache import cache

class MyUser:
    def __init__(self, user: CustomUser = None, token: str = None, telegram_id: str = None, debug: bool = False):
        self.user = user
        self.token = token
        self.telegram_id = telegram_id
        try:
            if self.user == None and self.token != None:
                user_id = cache.get(self.token)
                self.user = CustomUser.objects.get(id=user_id)
            if self.user == None and self.telegram_id != None:
                self.user = CustomUser.objects.get(telegram_user__chat_id=self.telegram_id)
        except Exception as e:
            print(e)
            return False
        if self.user == None and self.token == None and self.telegram_id == None and not debug:
            return False

    def merge_telegram(self, shema: TelegramShema.MergeTelegram):
        return self.user.add_telegram_to_user(shema)
    
    def merge_phone(self, shema: TelegramShema.MergePhone):
        return self.user.add_phone_to_user(shema)
    
    def angry_test(self):
        user = CustomUser.objects.last() #! только для тестового кейса
        return user.generate_token_to_cache()
