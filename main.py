import os
import asyncio
import logging
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
import uvicorn

# Токен твоего бота (не забудь сменить через BotFather в целях безопасности)
TOKEN = os.getenv("BOT_TOKEN", "8882324836:AAHyS_mGX1OzgxtuQSlKNCT3c2PfYb_wock")

# Список твоих чатов (взяты из предоставленных ссылок)
CHAT_IDS = [
    -1001375624726,
    -1001438298429,
    -1001250590505,
    -1001442937604
]

# Рекламное сообщение с твоими услугами
SERVICES_MESSAGE = (
    "🚀 **ПРОФЕССИОНАЛЬНАЯ РАЗРАБОТКА И IT-УСЛУГИ** 🚀\n\n"
    "Ищете качественное решение под ключ? Мы создаем цифровые продукты:\n\n"
    "🤖 **Telegram-боты** — от простых автоответчиков до сложных платформ.\n"
    "📱 **Telegram Mini Apps** — интерактивные веб-приложения внутри мессенджера.\n"
    "💻 **Сайты под ключ** — лендинги, интернет-магазины, порталы.\n"
    "🛒 **Дизайн карточек для маркетплейсов** — продающая инфографика для Wildberries и Ozon.\n"
    "☁️ **Настройка хостинга** — перенос проектов, обеспечение стабильной работы 24/7.\n\n"
    "✨ Быстро, качественно и по доступной цене!\n"
    "📩 По всем вопросам: пишите в личные сообщения @serjantyabloko"
    "serjanyabloko.github.io"
)

# Инициализация бота
bot = Bot(token=TOKEN)

# Настройка FastAPI для удержания сервера на Fly.io живым
app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "Multi-chat bot is running 24/7!"}

async def send_scheduled_message():
    """Функция циклической рассылки по всем указанным чатам раз в час"""
    for chat_id in CHAT_IDS:
        try:
            await bot.send_message(chat_id=chat_id, text=SERVICES_MESSAGE, parse_mode="Markdown")
            print(f"Сообщение успешно отправлено в чат: {chat_id}")
            # Небольшая пауза между отправками, чтобы не получить спам-блок
            await asyncio.sleep(0.5)
        except Exception as e:
            print(f"Ошибка при отправке в чат {chat_id}: {e}")

async def run_scheduler():
    scheduler = AsyncIOScheduler()
    # Запуск задачи каждые 3600 секунд (ровно 1 час)
    scheduler.add_job(send_scheduled_message, 'interval', seconds=3600)
    scheduler.start()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_scheduler())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
