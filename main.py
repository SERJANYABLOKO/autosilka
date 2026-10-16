import os
import asyncio
import logging
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
import uvicorn

# Читаем токен (если переменная окружения не задана, подставим твой текущий токен)
TOKEN = os.getenv("BOT_TOKEN", "8882324836:AAHyS_mGX1OzgxtuQSlKNCT3c2PfYb_wock")
# ID чата, куда бот будет отправлять рекламное сообщение раз в час
CHAT_ID = os.getenv("CHAT_ID", "ТВОЙ_ID_ЧАТА")

# Красивое оформление сообщения с услугами
SERVICES_MESSAGE = (
    "🚀 **ПРОФЕССИОНАЛЬНАЯ РАЗРАБОТКА И IT-УСЛУГИ** 🚀\n\n"
    "Ищете качественное решение под ключ? Мы создаем цифровые продукты любой сложности:\n\n"
    "🤖 **Telegram-боты** — от простых автоответчиков до сложных CRM-систем и платформ.\n"
    "📱 **Telegram Mini Apps** — интерактивные веб-приложения прямо внутри мессенджера.\n"
    "💻 **Сайты под ключ** — лендинги, интернет-магазины, корпоративные сайты.\n"
    "🛒 **Дизайн карточек для маркетплейсов** — продающая инфографика для Wildberries и Ozon.\n"
    "☁️ **Настройка хостинга** — перенос проектов на серверы, настройка бесперебойной работы 24/7.\n\n"
    "✨ **Почему выбирают нас?** Быстро, качественно и по доступной цене!\n"
    "📩 По всем вопросам: пишите в личные сообщения!"
)

# Инициализация бота
bot = Bot(token=TOKEN)

# Настройка FastAPI для удержания сервера на Fly.io живым
app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "Bot is running online 24/7!"}

async def send_scheduled_message():
    """Функция отправки рекламного сообщения раз в час"""
    try:
        await bot.send_message(chat_id=CHAT_ID, text=SERVICES_MESSAGE, parse_mode="Markdown")
        print("Сообщение с услугами успешно отправлено!")
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")

async def run_scheduler():
    """Запуск планировщика задач"""
    scheduler = AsyncIOScheduler()
    # Отправка ровно каждый 1 час (3600 секунд)
    scheduler.add_job(send_scheduled_message, 'interval', seconds=3600)
    scheduler.start()

@app.on_event("startup")
on_startup = lambda: asyncio.create_task(run_scheduler())

if __name__ == "__main__":
    # Запуск веб-сервера (требуется для Fly.io, чтобы сервис считался Web-приложением)
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
