from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from pathlib import Path

LECTURES_DIR = Path(__file__).parent.parent / "lectures"


def subjects_keyboard():
    builder = InlineKeyboardBuilder()
    subjects = [p.name for p in LECTURES_DIR.iterdir() if p.is_dir()]
    for sub in subjects:
        builder.button(text=sub.capitalize(), callback_data=f"subject:{sub}")
    builder.adjust(2)
    return builder.as_markup()


def lectures_keyboard(subject: str):
    builder = InlineKeyboardBuilder()
    path = LECTURES_DIR / subject
    if path.exists():
        for f in path.iterdir():
            if f.suffix == ".txt":
                builder.button(text=f.stem, callback_data=f"lecture:{subject}:{f.stem}")
    else:
        builder.button(text="Лекций нет", callback_data="lecture:none")
    builder.adjust(2)
    return builder.as_markup()


def back_keyboard(subject: str):
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅ Назад к лекциям", callback_data=f"back_lectures:{subject}")
    builder.button(text="🔄 Сменить предмет", callback_data="back_subjects")
    builder.adjust(2)
    return builder.as_markup()
