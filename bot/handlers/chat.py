from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

from bot.services.llm_client import llm_client
from bot.keyboards import subjects_keyboard, lectures_keyboard


router = Router()
user_sessions = {}


async def clear_last_keyboard(bot, chat_id, session: dict):
    msg_id = session.get("last_keyboard_msg_id")
    if not msg_id:
        return
    try:
        await bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=msg_id,
            reply_markup=None
        )
    except Exception:
        pass


def save_keyboard_msg(session: dict, msg: Message):
    session["last_keyboard_msg_id"] = msg.message_id


@router.message(Command(commands=["start"]))
async def start_handler(message: Message):
    user_sessions[message.from_user.id] = {}
    await message.answer("Выберите предмет:", reply_markup=subjects_keyboard())


@router.callback_query(F.data.startswith("subject:"))
async def subject_callback(call: CallbackQuery):
    user_id = call.from_user.id
    subject = call.data.split(":")[1]

    session = user_sessions.setdefault(user_id, {})
    session.update({"subject": subject, "lecture": None})

    keyboard = lectures_keyboard(subject)
    keyboard.inline_keyboard.append(
        [InlineKeyboardButton(text="⬅ Назад к предметам", callback_data="back_subjects")]
    )

    await call.message.edit_text(f"Выбран предмет: {subject}. Выберите лекцию:")
    await call.message.edit_reply_markup(reply_markup=keyboard)

    save_keyboard_msg(session, call.message)
    await call.answer()


@router.callback_query(F.data.startswith("lecture:"))
async def lecture_callback(call: CallbackQuery):
    user_id = call.from_user.id
    _, subject, lecture = call.data.split(":")

    session = user_sessions[user_id]
    session["lecture"] = lecture

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅ Назад к лекциям", callback_data=f"back_lectures:{subject}")]
    ])

    await call.message.edit_text(
        f"Выбрана лекция {lecture}\nпо предмету {subject}\nСпросите меня по ней:",
        reply_markup=keyboard
    )

    save_keyboard_msg(session, call.message)
    await call.answer()


@router.callback_query(F.data.startswith("back_lectures:"))
async def back_lectures_callback(call: CallbackQuery):
    user_id = call.from_user.id
    subject = call.data.split(":")[1]

    session = user_sessions[user_id]
    session["lecture"] = None

    keyboard = lectures_keyboard(subject)
    keyboard.inline_keyboard.append(
        [InlineKeyboardButton(text="⬅ Назад к предметам", callback_data="back_subjects")]
    )

    await call.message.edit_text(f"Выберите лекцию для предмета {subject}:")
    await call.message.edit_reply_markup(reply_markup=keyboard)

    save_keyboard_msg(session, call.message)
    await call.answer()


@router.callback_query(F.data == "back_subjects")
async def back_subjects_callback(call: CallbackQuery):
    user_id = call.from_user.id
    user_sessions[user_id] = {}

    await call.message.edit_text("Выберите предмет:")
    await call.message.edit_reply_markup(reply_markup=subjects_keyboard())

    save_keyboard_msg(user_sessions[user_id], call.message)
    await call.answer()


@router.message()
async def chat_handler(message: Message):
    user_id = message.from_user.id
    text = message.text

    session = user_sessions.get(user_id)
    if not session or not session.get("lecture"):
        await message.answer("Сначала выберите предмет и лекцию командой /start")
        return

    subject = session["subject"]
    lecture = session["lecture"]

    await clear_last_keyboard(message.bot, message.chat.id, session)

    waiting_msg = await message.answer("⏳ Ожидание ответа от LLM...")

    reply = await llm_client.chat(
        user_id=user_id,
        text=text,
        subject=subject,
        lecture=lecture
    )

    await waiting_msg.edit_text(reply)

    keyboard_msg = await message.answer(
        f"Выбрана лекция {lecture}\nпо предмету {subject}\nСпросите меня по ней:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="⬅ Назад к лекциям",
                callback_data=f"back_lectures:{subject}"
            )]
        ])
    )

    save_keyboard_msg(session, keyboard_msg)
