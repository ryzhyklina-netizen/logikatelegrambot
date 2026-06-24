import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import TelegramError
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)


# ---------------------------------------------------------
# ОСНОВНІ НАЛАШТУВАННЯ
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR / "images"
WELCOME_IMAGE = IMAGES_DIR / "main.png"

# load_dotenv(BASE_DIR / ".env")
# BOT_TOKEN = os.getenv("BOT_TOKEN")

from dotenv import load_dotenv

# тільки для локального запуску
if (BASE_DIR / ".env").exists():
    load_dotenv(BASE_DIR / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# ЗАПИТАННЯ ТЕСТУ
# correct — номер правильної відповіді:
# 0 = перший варіант
# 1 = другий варіант
# 2 = третій варіант
# 3 = четвертий варіант
# ---------------------------------------------------------

QUESTIONS = [
    # A0
    {
        "text": (
            "1/25. Доповніть речення:\n\n"
            "___ is Taylor Swift."
        ),
        "options": ["He", "She", "It", "They"],
        "correct": 1,
        "level": "A0",
    },
    {
        "text": (
            "2/25. Доповніть речення:\n\n"
            "Lionel Messi ___ a famous football player."
        ),
        "options": ["am", "are", "is", "be"],
        "correct": 2,
        "level": "A0",
    },
    {
        "text": (
            "3/25. Доповніть речення:\n\n"
            "Zendaya ___ many fans around the world."
        ),
        "options": ["have", "has", "is", "having"],
        "correct": 1,
        "level": "A0",
    },
    {
        "text": (
            "4/25. Доповніть речення:\n\n"
            "Ariana Grande is a famous ___."
        ),
        "options": ["singer", "doctor", "teacher", "driver"],
        "correct": 0,
        "level": "A0",
    },
    {
        "text": (
            "5/25. Доповніть речення:\n\n"
            "The singer ___ now."
        ),
        "options": ["sings", "sing", "is singing", "are singing"],
        "correct": 2,
        "level": "A0",
    },

    # A1
    {
        "text": (
            "6/25. Доповніть речення:\n\n"
            "Emma Watson ___ in every Harry Potter film now."
        ),
        "options": [
            "doesn’t act",
            "don’t act",
            "isn’t act",
            "not acts",
        ],
        "correct": 0,
        "level": "A1",
    },
    {
        "text": (
            "7/25. Доповніть питання:\n\n"
            "___ Billie Eilish write songs?"
        ),
        "options": ["Is", "Does", "Do", "Has"],
        "correct": 1,
        "level": "A1",
    },
    {
        "text": (
            "8/25. Оберіть правильний переклад:\n\n"
            "«Він працював у лікарні»."
        ),
        "options": [
            "He work in a hospital.",
            "He did worked in a hospital.",
            "He worked in a hospital.",
            "He has work in a hospital.",
        ],
        "correct": 2,
        "level": "A1",
    },
    {
        "text": (
            "9/25. Оберіть правильне питання:\n\n"
            "«Before filming a movie, an actor learns the ___.»"
        ),
        "options": [
            "menu",
            "lines",
            "ticket",
            "recipe",
        ],
        "correct": 1,
        "level": "A1",
    },
    {
        "text": (
            "10/25. Оберіть правильний переклад:\n\n"
            "«Чи хотіли б ви зустрітися з улюбленим актором?»"
        ),
        "options": [
            "Would you like meet your favourite actor?",
            "Would you like meeting your favourite actor?",
            "Would you like to meet your favourite actor?",
            "Do you would like to meet your favourite actor?",
        ],
        "correct": 2,
        "level": "A1",
    },

    # A2
    {
        "text": (
            "11/25. Доповніть речення:\n\n"
            "He ___ travel to Italy next week."
        ),
        "options": [
            "is going to",
            "will going",
            "goes to",
            "is go to",
        ],
        "correct": 0,
        "level": "A2",
    },
    {
        "text": (
            "12/25. Доповніть речення:\n\n"
            "Adele ___ many successful songs."
        ),
        "options": [
            "writes",
            "wrote",
            "has written",
            "is writing",
        ],
        "correct": 2,
        "level": "A2",
    },
    {
        "text": (
            "13/25. Доповніть речення:\n\n"
            "Have you ___ seen a celebrity in real life?"
        ),
        "options": ["already", "ever", "yet", "never"],
        "correct": 1,
        "level": "A2",
    },
    {
        "text": (
            "14/25. Оберіть правильне значення виділеного слова:\n\n"
            "The concert was CROWDED."
        ),
        "options": [
            "very quiet",
            "full of people",
            "very expensive",
            "badly organised",
        ],
        "correct": 1,
        "level": "A2",
    },
    {
        "text": (
            "15/25. Доповніть речення:\n\n"
            "If Tom Holland ___ another superhero film, "
            "many people will watch it."
        ),
        "options": [
            "makes",
            "will make",
            "made",
            "is make",
        ],
        "correct": 0,
        "level": "A2",
    },

    # B1
    {
        "text": (
            "16/25. Доповніть речення:\n\n"
            "The director ___ on the new film for several months."
        ),
        "options": [
            "works",
            "has worked",
            "has been working",
            "was worked",
        ],
        "correct": 2,
        "level": "B1",
    },
    {
        "text": (
            "17/25. Доповніть речення:\n\n"
            "Sherlock Holmes ___ the case when he suddenly "
            "___ an important clue."
        ),
        "options": [
            "solved / was noticing",
            "was investigating / found",
            "investigated / was finding",
            "has investigated / finds",
        ],
        "correct": 1,
        "level": "B1",
    },
    {
        "text": (
            "18/25. Доповніть речення:\n\n"
            "Taylor Swift is a singer ___ has won many awards."
        ),
        "options": ["which", "where", "who", "whose"],
        "correct": 2,
        "level": "B1",
    },
    {
        "text": (
            "19/25. Оберіть правильний варіант:\n\n"
            "Will Smith had to ___ the interview because she was ill."
        ),
        "options": [
            "turn up",
            "put off",
            "look after",
            "find out",
        ],
        "correct": 1,
        "level": "B1",
    },
    {
        "text": (
            "20/25. Доповніть речення:\n\n"
            "If I ___ a famous actor, I would choose interesting roles."
        ),
        "options": ["am", "will be", "were", "have been"],
        "correct": 2,
        "level": "B1",
    },

    # B2
    {
        "text": (
            "21/25. Доповніть речення:\n\n"
            "If the actor had accepted the role, he ___ in the film."
        ),
        "options": [
            "would appear",
            "would have appeared",
            "appeared",
            "had appeared",
        ],
        "correct": 1,
        "level": "B2",
    },
    {
        "text": (
            "22/25. Доповніть речення:\n\n"
            "The organisers ___ the guests about the change earlier."
        ),
        "options": [
            "should inform",
            "should have informed",
            "should informed",
            "had to informed",
        ],
        "correct": 1,
        "level": "B2",
    },
    {
        "text": (
            "23/25. Доповніть речення:\n\n"
            "___ she wins the award or not, "
            "she has already achieved a lot."
        ),
        "options": [
            "Despite",
            "Although",
            "Whether",
            "However",
        ],
        "correct": 2,
        "level": "B2",
    },
    {
        "text": (
            "24/25. Оберіть слово, яке найкраще доповнює речення:\n\n"
            "The actor gave a remarkably ___ performance "
            "that impressed both critics and audiences."
        ),
        "options": [
            "compelling",
            "ordinary",
            "careless",
            "irrelevant",
        ],
        "correct": 0,
        "level": "B2",
    },
    {
        "text": (
            "25/25. Доповніть речення:\n\n"
            "If she had accepted that job last year, "
            "she ___ in New York now."
        ),
        "options": [
            "would live",
            "would have lived",
            "would be living",
            "lived",
        ],
        "correct": 2,
        "level": "B2",
    },
]


# ---------------------------------------------------------
# ДОПОМІЖНІ ФУНКЦІЇ
# ---------------------------------------------------------

def determine_level(score: int) -> str:
    """Визначає орієнтовний рівень за кількістю правильних відповідей."""
    if score <= 5:
        return "A0"
    if score <= 10:
        return "A1"
    if score <= 15:
        return "A2"
    if score <= 20:
        return "B1"
    return "B2"


def get_image_path(question_index: int) -> Path:
    """Повертає шлях до картинки певного запитання."""
    return IMAGES_DIR / f"{question_index + 1}.png"


def make_start_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                "🚀 Почати тест",
                callback_data="start_test",
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def make_question_keyboard(
    question_index: int,
    options: list[str],
) -> InlineKeyboardMarkup:
    """Створює чотири кнопки-відповіді та кнопку «Не знаю»."""
    keyboard = []

    for option_index, option in enumerate(options):
        keyboard.append(
            [
                InlineKeyboardButton(
                    option,
                    callback_data=(
                        f"answer:{question_index}:{option_index}"
                    ),
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "🤷 Не знаю відповіді",
                callback_data=f"answer:{question_index}:unknown",
            )
        ]
    )

    return InlineKeyboardMarkup(keyboard)


# ---------------------------------------------------------
# КОМАНДА /START
# ---------------------------------------------------------

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    context.user_data.clear()

    caption = (
        "🎓 Визнач свій рівень англійської разом із Logika!\n\n"
        "Цей тест створено Всеукраїнською школою програмування "
        "та англійської мови Logika 💜\n\n"
        f"На тебе чекають {len(QUESTIONS)} запитань - "
        "від простих до складніших.\n\n"
        "Обирай «Не знаю відповіді», якщо не впевнений. "
        "Так результат буде точнішим.\n\n"
        "Бажаємо успіху! 🚀"
    )

    if update.message is None:
        return

    if WELCOME_IMAGE.exists():
        with WELCOME_IMAGE.open("rb") as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=caption,
                reply_markup=make_start_keyboard(),
            )
    else:
        await update.message.reply_text(
            caption,
            reply_markup=make_start_keyboard(),
        )


# ---------------------------------------------------------
# НАДСИЛАННЯ ЗАПИТАННЯ
# ---------------------------------------------------------

async def send_question(
    chat_id: int,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    question_index = context.user_data.get("question_index", 0)

    if question_index >= len(QUESTIONS):
        return

    question = QUESTIONS[question_index]
    image_path = get_image_path(question_index)

    keyboard = make_question_keyboard(
        question_index,
        question["options"],
    )

    if image_path.exists():
        with image_path.open("rb") as photo:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=question["text"],
                reply_markup=keyboard,
            )
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                f"{question['text']}\n\n"
                f"⚠️ Не знайдено картинку: {image_path.name}"
            ),
            reply_markup=keyboard,
        )


# ---------------------------------------------------------
# ФІНАЛЬНИЙ РЕЗУЛЬТАТ
# ---------------------------------------------------------

async def send_result(
    chat_id: int,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    score = context.user_data.get("score", 0)
    unknown_count = context.user_data.get("unknown_count", 0)
    level = determine_level(score)

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔄 Пройти тест ще раз",
                    callback_data="start_test",
                )
            ]
        ]
    )

    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            "🎉 Тест завершено!\n\n"
            f"✅ Правильних відповідей: {score} із {len(QUESTIONS)}\n"
            f"🤷 Відповідей «Не знаю»: {unknown_count}\n\n"
            f"Твій орієнтовний рівень англійської — "
            f"⭐ {level} ⭐\n\n"
            "Результат тесту є орієнтовним. "
            "З нетерпінням чекатимемо тебе на "
            "наших заняттях у школі Logika 💜"
        ),
        reply_markup=keyboard,
    )


# ---------------------------------------------------------
# ОБРОБКА КНОПОК
# ---------------------------------------------------------

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    query = update.callback_query
    
    if query is None:
        return

    await query.answer()

    if query.message is None:
        return

    data = query.data or ""
    chat_id = query.message.chat.id
    # Початок або повторне проходження тесту
    if data == "start_test":
        context.user_data.clear()
        context.user_data["score"] = 0
        context.user_data["unknown_count"] = 0
        context.user_data["question_index"] = 0

        try:
            await query.message.delete()
        except TelegramError:
            pass

        await send_question(chat_id, context)
        return

    # Обробка відповіді
    if not data.startswith("answer:"):
        return

    parts = data.split(":")

    if len(parts) != 3:
        return

    try:
        button_question_index = int(parts[1])
    except ValueError:
        return

    current_question_index = context.user_data.get("question_index")

    if current_question_index is None:
        await query.answer(
            "Тест не запущено. Натисни /start.",
            show_alert=True,
        )
        return

    # Захист від повторного натискання старої кнопки
    if button_question_index != current_question_index:
        await query.answer(
            "Ця відповідь уже неактивна.",
            show_alert=False,
        )
        return

    question = QUESTIONS[current_question_index]
    selected_value = parts[2]

    if selected_value == "unknown":
        context.user_data["unknown_count"] += 1
    else:
        try:
            selected_option = int(selected_value)
        except ValueError:
            return

        if selected_option == question["correct"]:
            context.user_data["score"] += 1

    # Переходимо до наступного питання
    context.user_data["question_index"] += 1

    try:
        await query.message.delete()
    except TelegramError:
        pass

    if context.user_data["question_index"] < len(QUESTIONS):
        await send_question(chat_id, context)
    else:
        await send_result(chat_id, context)


# ---------------------------------------------------------
# ОБРОБКА ПОМИЛОК
# ---------------------------------------------------------

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    logger.exception(
        "Під час роботи бота сталася помилка:",
        exc_info=context.error,
    )


# ---------------------------------------------------------
# ЗАПУСК БОТА
# ---------------------------------------------------------

def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError(
            "Не знайдено BOT_TOKEN. Перевір файл .env."
        )

    if not IMAGES_DIR.exists():
        raise RuntimeError(
            "Не знайдено папку images."
        )

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("restart", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_error_handler(error_handler)

    print("✅ Бот запущений!")
    print("Для зупинки натисни Ctrl+C.")

    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()