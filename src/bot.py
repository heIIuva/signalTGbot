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

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# Путь к видеофайлу в папке assets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_PATH = os.path.join(BASE_DIR, '..', 'assets', 'welcome.mp4')

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    logger.info(f"Получена команда от пользователя {message.from_user.id}: {message.text}")
    
    # Формируем подпись
    caption_text = f"Hello, {message.from_user.first_name}\nNow we can be friends and start earning together, I need motivated people!\n\n✅ GET HACK BOT FREE ✅\n\nWithout saying too much, I made a video for you and gave you brief instructions on how to earn your first 100$ using a bot:"
    
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

logger.info("Бот запускается...")
try:
    bot.polling(none_stop=True, timeout=60)
    logger.info("Бот успешно запущен")
except Exception as e:
    logger.error(f"Ошибка при запуске бота: {e}")
