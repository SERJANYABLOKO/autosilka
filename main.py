import os
import asyncio
import logging
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
import uvicorn

# Получаем настройки из переменных окружения Fly.io (или подставь свои значения для теста)
TOKEN = os.getenv("BOT_TOKEN", "ТВОЙ_ТОКЕН_БОТА")
CHAT_ID = os.getenv("CHAT_ID", "ID_ЧАТА_ИЛИ_КАНАЛА")
MESSAGE_TEXT = "Привет! Это автоматическое сообщение каждый час."
PORT = int(os.getenv("PORT", 8080))

# Инициализация бота, планировщика и веб-приложения
bot = Bot(token=TOKEN)
scheduler = AsyncIOScheduler()
app = FastAPI()

@app.get("/")
async def health_check():
    """Эндпоинт для проверки здоровья, чтобы Fly.io понимал, что приложение живое"""
    return {"status": "ok", "message": "Bot is running!"}

async def send_scheduled_message():
    """Функция отправки сообщения"""
    try:
        await bot.send_message(chat_id=CHAT_ID, text=MESSAGE_TEXT)
        logging.info("Сообщение успешно отправлено!")
    except Exception as e:
        logging.error(f"Ошибка при отправке: {e}")

async def run_bot():
    logging.basicConfig(level=logging.INFO)
    
    # Настраиваем задачу: отправка каждый час (3600 секунд)
    scheduler.add_job(send_scheduled_message, 'interval', seconds=3600)
    scheduler.start()
    logging.info("Планировщик запущен. Ожидание отправки...")
    
    # Сбрасываем старые апдейты
    await bot.delete_webhook(drop_pending_updates=True)

@app.on_event("startup")
async def on_startup():
    # Запускаем планировщик при старте FastAPI сервера
    asyncio.create_task(run_bot())

if __name__ == "__main__":
    # Запуск сервера через uvicorn (Fly.io требует открытый порт)
    uvicorn.run("bot:app", host="0.0.0.0", port=PORT)
