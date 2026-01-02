from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.keyboards import subjects_keyboard


router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Привет!\n"
        "Я бот-помощник по лекциям БМТ\n"
        "Выберите предмет, чтобы начать работу с лекциями:",
        reply_markup=subjects_keyboard()
    )
