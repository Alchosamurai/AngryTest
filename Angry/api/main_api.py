from ninja import NinjaAPI
from django.http import HttpResponse
from api.shemas import TelegramShema
from auth_app.my_user import MyUser
import environ
import os
env = environ.Env()
environ.Env.read_env()
environ.Env.read_env(os.path.join("/Users/nikitaaniskevic/Dev/Angry/AngryTest/", '.env'))

api = NinjaAPI()

@api.post("/merge-telegram", tags=["Telegram"],summary="Add telegram to user")
def merge_telegram(request, shema: TelegramShema.MergeTelegram):
    check_key(shema.api_key)
    status =MyUser(token = shema.token).merge_telegram(shema)
    return check_status(status)

@api.post("/merge-phone", tags=["Telegram"], summary="Add phone to user")
def merge_phone(request, shema: TelegramShema.MergePhone):
    check_key(shema.api_key)
    status = MyUser(telegram_id = shema.telegram_id).merge_phone(shema)
    return HttpResponse({"status": 200})
@api.get("/generate-tg-link", tags=["Telegram"], summary="Generate tg link")
def generate_tg_link(request):
    token = MyUser(debug=True).angry_test()
    #* пусть будет юзер с id 1 для ускорения написания тестового
    link = f"https://t.me/{env("BOT_NAME")}?start={token}"
    return link
#* много времени уже ушло для тестового, так не буду делать страничку для привязки, обойдемся обычной ссылкой 

def check_key(key):
    if key != env("API_KEY"):
        return HttpResponse({"status": 400, "error": "Invalid API key"}, status=400)
def check_status(status):
    if status:
        return HttpResponse({"status": 200})
    return HttpResponse({"status": 400, "error": "Unexpected error"}, status=400)


