import json
import urllib.request
import urllib.parse

# Твой токен и список из 5 чатов
TOKEN = "8882324836:AAHyS_mGX1OzgxtuQSlKNCT3c2PfYb_wock"
CHAT_IDS = [
    -1001375624726,
    -1001438298429,
    -1001250590505,
    -1001442937604,
    -5255859989
]

SERVICES_MESSAGE = (
    "🚀 *ПРОФЕССИОНАЛЬНАЯ РАЗРАБОТКА И IT-УСЛУГИ* 🚀\n\n"
    "Ищете качественное решение под ключ? Мы создаем цифровые продукты:\n\n"
    "🤖 *Telegram-боты* — от простых автоответчиков до сложных платформ.\n"
    "📱 *Telegram Mini Apps* — интерактивные веб-приложения внутри мессенджера.\n"
    "💻 *Сайты под ключ* — лендинги, интернет-магазины, порталы.\n"
    "🛒 *Дизайн карточек для маркетплейсов* — продающая инфографика для Wildberries и Ozon.\n"
    "☁️ *Настройка хостинга* — перенос проектов, обеспечение стабильной работы 24/7.\n\n"
    "✨ Быстро, качественно и по доступной цене!\n"
    "📩 По всем вопросам: пишите в личные сообщения!"
)

def handler(event, context):
    success_count = 0
    errors = []

    for chat_id in CHAT_IDS:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": SERVICES_MESSAGE,
            "parse_mode": "Markdown"
        }
        
        data = urllib.parse.urlencode(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST")
        
        try:
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    success_count += 1
        except Exception as e:
            errors.append(f"Chat {chat_id}: {str(e)}")

    if errors:
        return {
            "statusCode": 500,
            "body": json.dumps({"success_count": success_count, "errors": errors})
        }

    return {
        "statusCode": 200,
        "body": json.dumps({"status": f"Successfully sent to {success_count} chats!"})
    }
