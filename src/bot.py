import telebot
import logging
import os
from pathlib import Path
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

dotenv_path = Path("/app/.env")

# Загружаем переменные окружения из файла .env
load_dotenv(dotenv_path=dotenv_path)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TOKEN")
PROMOCODE = os.getenv("PROMOCODE")
BASEURL = os.getenv("BASEURL")
CHANNEL_URL = os.getenv("CHANNEL_URL")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# Путь к видеофайлу в папке assets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_PATH = os.path.join(BASE_DIR, '..', 'assets', 'welcome.mp4')

# Антибот-функция для проверки наличия аватара или username
def has_profile_photo(user_id: int) -> bool:
    try:
        photos = bot.get_user_profile_photos(user_id, limit=1)
        return photos.total_count > 0
    except Exception as e:
        logger.warning(f"Не удалось проверить фото профиля {user_id}: {e}")
        return False

def is_real_user(u: telebot.types.User) -> bool:
    # Базовое правило: не бот + (есть username ИЛИ есть аватар)
    if u.is_bot:
        return False
    if u.username:
        return True
    return has_profile_photo(u.id)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    logger.info(f"Получена команда от пользователя {message.from_user.id}: {message.text}")
    
    # Формируем подпись
    caption_text = f"🔥🚀 Hello, {message.from_user.first_name}\nI’m glad you made it here. Not everyone gets access to this, so consider yourself lucky.\n\n✅ WELCOME BONUS ✅\n\nI won’t reveal too much here… Inside the channel you’ll get the real details and step-by-step instructions.\n\nJoin now and unlock your bonus!\n\n👉 Join the private channel using the link below"
    
    logger.info(f"Отправляем подпись: {caption_text}")
    
    # Создаем клавиатуру с кнопкой
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🔥JOIN PRIVATE CHANNEL🔥", url=f"{CHANNEL_URL}"))
    
    try:
        # Отправляем видео как анимацию (GIF) с подписью и кнопкой
        with open(VIDEO_PATH, 'rb') as gif:
            bot.send_animation(
                message.chat.id,
                gif,
                caption=caption_text,
                reply_markup=keyboard
            )
            logger.info("Анимация (GIF) с подписью и кнопкой успешно отправлена")
    except Exception as e:
        logger.error(f"Ошибка при отправке анимации: {e}")
        # Если анимация не удалось отправить, отправляем только текст с кнопкой
        try:
            bot.send_message(
                message.chat.id,
                f"Hello, {message.from_user.first_name}\nNow we can be friends and start earning together, I need motivated people!\n\n✅ GET HACK BOT FREE ✅\n\nWithout saying too much, I made a video for you and gave you brief instructions on how to earn your first 100$ using a bot:",
                reply_markup=keyboard
            )
            logger.info("Текстовое сообщение с кнопкой отправлено после ошибки с анимацией")
        except Exception as e2:
            logger.error(f"Ошибка при отправке текстового сообщения: {e2}")

# Обработчик всех текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    logger.info(f"Получено текстовое сообщение от {message.from_user.id}: {message.text}")
    try:
        bot.reply_to(message, f"Вы написали: {message.text}")
        logger.info("Эхо-сообщение успешно отправлено")
    except Exception as e:
        logger.error(f"Ошибка при отправке эхо-сообщения: {e}")

@bot.chat_join_request_handler(func=lambda r: True)
def handle_join_request(req: telebot.types.ChatJoinRequest):
    try:
        # фильтруем только наш канал (если бот админ сразу в нескольких)
        if CHANNEL_ID and req.chat.id != CHANNEL_ID:
            logger.info(f"Заявка не из целевого канала: chat_id={req.chat.id}")
            return

        user = req.from_user
        logger.info(f"Заявка на вступление: user_id={user.id}, username=@{user.username}, is_bot={user.is_bot}")

        if is_real_user(user):
            bot.approve_chat_join_request(req.chat.id, user.id)
            logger.info(f"Одобрили заявку user_id={user.id}")

            # Если юзер ранее нажимал /start у бота — можно уведомить в ЛС:
            try:
                bot.send_message(user.id, "✅ Ваша заявка одобрена. Добро пожаловать в канал!")
            except Exception as dm_err:
                # если не писал боту — будет 403; это нормально
                logger.debug(f"Не удалось отправить личное сообщение {user.id}: {dm_err}")
        else:
            bot.decline_chat_join_request(req.chat.id, user.id)
            logger.info(f"Отклонили заявку (похоже на бота) user_id={user.id}")
    except Exception as e:
        logger.error(f"Ошибка при обработке заявки: {e}")

logger.info("Бот запускается...")
try:
    bot.polling(none_stop=True, timeout=60, allowed_updates=['message', 'chat_join_request'])
    logger.info("Бот успешно запущен")
except Exception as e:
    logger.error(f"Ошибка при запуске бота: {e}")
