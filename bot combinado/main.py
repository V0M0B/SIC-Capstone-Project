import telebot as tlb
import os
from modules.voice_transcriber import handle_voice
from modules.link_checker import handle_link
#from modules.image_spam_detector import handle_image
#from modules.sentiment_analyzer import handle_text_sentiment
from dotenv import load_dotenv

load_dotenv()

#Configurando entorno de variables
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')


if not TELEGRAM_TOKEN:
    raise ValueError("No se encuentra el TOKEN de telegram en su archivo de variables de entorno .env")


# #Instanciar los objetos
bot = tlb.TeleBot(TELEGRAM_TOKEN)





# --- Handlers de los módulos ---
@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    handle_voice(bot, message)

@bot.message_handler(func=lambda msg: msg.text and "http" in msg.text)
def handle_link_message(message):
    handle_link(bot, message)


# @bot.message_handler(content_types=['photo'])
# def handle_photo_message(message):
#     handle_image(bot, message)

# @bot.message_handler(content_types=['text'])
# def handle_text_message(message):
#     handle_text_sentiment(bot, message)

# --- Iniciar bot ---
print("🤖 Bot multipropósito en ejecución...")
bot.infinity_polling()