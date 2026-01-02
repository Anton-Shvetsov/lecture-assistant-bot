from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import settings
from bot.handlers import start, chat
from bot.middlewares.errors import ErrorMiddleware


async def create_app():
    bot = Bot(
        token=settings.telegram_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        ),
    )

    dp = Dispatcher()
    dp.message.middleware(ErrorMiddleware())

    dp.include_router(start.router)
    dp.include_router(chat.router)

    await dp.start_polling(bot)
