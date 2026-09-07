import os
import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# --- Настройка логирования ---
logging.basicConfig(level=logging.INFO)

# --- Загрузка токена из переменных окружения ---
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    logging.error("❌ Ошибка: Переменная TELEGRAM_TOKEN не найдена!")
    exit(1)

# --- Инициализация бота ---
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- Обработчик команды /start ---
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}! Бот работает на Render через polling!")

# --- Health-check для Render ---
async def health_check(request):
    return web.Response(text="Bot is running!")

# --- Функция для запуска веб-сервера ---
async def run_webserver():
    app = web.Application()
    app.router.add_get("/", health_check)  # Эндпоинт для проверки

    port = int(os.environ.get("PORT", 8080))  # Порт от Render
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=port)
    await site.start()
    logging.info(f"✅ Веб-сервер запущен на порту {port}")

    # Бесконечно ждем, чтобы сервер не завершился
    await asyncio.Event().wait()

# --- Запуск бота в режиме polling ---
async def run_bot():
    logging.info("🚀 Бот запускается в режиме polling...")
    await dp.start_polling(bot)

# --- Главная функция ---
async def main():
    # Запускаем бота и веб-сервер параллельно
    await asyncio.gather(
        run_bot(),
        run_webserver()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("👋 Бот остановлен.")