import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
from aiogram.client.session.aiohttp import AiohttpSession


# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Получаем токен
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env файле")


proxy_session = AiohttpSession(proxy="socks5://127.0.0.1:1080")

# Создаем экземпляры бота и диспетчера
bot = Bot(token=BOT_TOKEN, session=proxy_session)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привет! Я бот-напоминалка.\n\n"
        "Бот работает и готов к использованию!\n"
        "Для проверки отправь /help"
    )

# Обработчик команды /help
@dp.message(Command('help'))
async def cmd_help(message: types.Message):
    await message.answer(
        "📋 Доступные команды:\n"
        "/start - Приветствие\n"
        "/help - Помощь\n"
        "/ping - Проверка работы бота\n"
        "/echo <текст> - Повторить текст"
    )

# Обработчик команды /ping
@dp.message(Command('ping'))
async def cmd_ping(message: types.Message):
    await message.answer("🏓 Pong!")

# Обработчик команды /echo
@dp.message(Command('echo'))
async def cmd_echo(message: types.Message):
    # Получаем текст после команды
    text = message.text.replace('/echo', '').strip()
    if text:
        await message.answer(f"🔊 {text}")
    else:
        await message.answer("ℹ️ Напиши текст после команды /echo")

# Обработчик всех остальных сообщений
@dp.message()
async def handle_other_messages(message: types.Message):
    await message.answer(
        "🤔 Я не знаю такой команды.\n"
        "Используй /help для списка команд"
    )

# Функция запуска бота
async def main():
    logging.info("🚀 Запуск бота...")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"❌ Ошибка: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())