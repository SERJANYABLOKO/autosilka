import json
import asyncio
from aiogram import Bot

TOKEN = "8882324836:AAHyS_mGX1OzgxtuQSlKNCT3c2PfYb_wock"
CHAT_IDS = [-1001375624726, -1001438298429, -1001250590505, -1001442937604]

SERVICES_MESSAGE = (
    "🚀 **ПРОФЕССИОНАЛЬНАЯ РАЗРАБОТКА И IT-УСЛУГИ** 🚀\n\n"
    "Ищете качественное решение под ключ? Мы создаем цифровые продукты:\n\n"
    "🤖 **Telegram-боты** — от простых автоответчиков до сложных платформ.\n"
    "📱 **Telegram Mini Apps** — интерактивные веб-приложения внутри мессенджера.\n"
    "💻 **Сайты под ключ** — лендинги, интернет-магазины, порталы.\n"
    "🛒 **Дизайн карточек для маркетплейсов** — продающая инфографика для Wildberries и Ozon.\n"
    "☁️ **Настройка хостинга** — перенос проектов, обеспечение стабильной работы 24/7.\n\n"
    "✨ Быстро, качественно и по доступной цене!\n"
    "📩 По всем вопросам: пишите в личные сообщения!"
)

bot = Bot(token=TOKEN)

async def send_messages():
    for chat_id in CHAT_IDS:
        try:
            await bot.send_message(chat_id=chat_id, text=SERVICES_MESSAGE, parse_mode="Markdown")
            await asyncio.sleep(0.5)
        except Exception as e:
            print(f"Ошибка: {e}")

def handler(event, context):
    # Запуск отправки сообщений при запросе к функции
    asyncio.run(send_messages())

    return {
        "statusCode": 200,
        "body": json.dumps({"status": "Messages sent successfully!"})
    }
