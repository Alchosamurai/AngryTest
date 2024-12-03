
from ninja import Schema

class MergeTelegram(Schema):
    telegram_id: str
    username: str
    full_name: str
    token: str
    api_key: str

class MergePhone(Schema):
    telegram_id: str
    phone: str
    api_key: str