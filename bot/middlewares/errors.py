import logging
from aiogram import BaseMiddleware
from aiogram.types import Message


class ErrorMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        try:
            return await handler(event, data)
        except Exception as e:
            logging.exception("Unhandled error", exc_info=e)

            if isinstance(event, Message):
                await event.answer("⚠️ Произошла ошибка. Попробуй позже.")
