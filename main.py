# 1. Установите дополнительные зависимости
# pip install aiohttp aiogram-webhook

# 2. Добавьте webhook код:

from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.webhook.aiohttp_server import SimpleWebhookApp, setup_application

# Ваш бот
bot = Bot(token="YOUR_TOKEN")
dp = Dispatcher()

# Хендлеры как обычно
@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)

async def on_startup(bot: Bot):
    # Устанавливаем вебхук при запуске
    await bot.set_webhook("https://your-render-url.com/webhook")

async def on_shutdown(bot: Bot):
    # Удаляем вебхук при остановке
    await bot.delete_webhook()

async def main():
    # Создаем вебхук приложение
    webhook_router = SimpleWebhookApp(
        dispatcher=dp,
        bot=bot,
        webhook_path="/webhook",
        secret_token="your-secret"
    )
    
    # Создаем aiohttp приложение
    app = web.Application()
    app.router.register_resource(webhook_router)
    
    # Добавляем хендлеры для startup/shutdown
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    
    # Запускаем
    port = int(os.getenv("PORT", 8080))
    return app

if __name__ == "__main__":
    web.run_app(main(), host="0.0.0.0", port=int(os.getenv("PORT", 8080)))