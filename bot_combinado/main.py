#BOT COMBINADO (Análisis de imagen, Procesamiento de audio, Análisis de sentimiento, Integración de API URL) + CIBERBOT IA (Groq + Dataset)

#Importaciones base
import os
import json
import requests
import unicodedata
import re
from difflib import SequenceMatcher
from transformers import pipeline
from dotenv import load_dotenv
import telebot as tlb
from groq import Groq

# Módulos locales
from modules.voice_transcriber import handle_voice
from modules.link_checker import handle_link
from modules.sentiment_analyzer import cargar_analizador_sentimiento, analizar_texto
from modules.logica import buscar_en_dataset, es_relacionada, respuesta_groq
from modules.image_spam_detector import manejar_foto

# Cargar variables de entorno
load_dotenv()

# Tokens y API keys
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

if not TELEGRAM_TOKEN:
    raise ValueError("No se encuentra el TOKEN de telegram en su archivo de variables de entorno .env")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY no está configurado en las variables de entorno")

# Crear cliente Groq pra su funcionamiento
cliente_groq = Groq(api_key=GROQ_API_KEY)

# Ruta al archivo JSON que contiene el dataset de preguntas y respuestas
DATASET_PATH = "bot_combinado/dataset.json"

# Crear instancia del bot de telegram
bot = tlb.TeleBot(TELEGRAM_TOKEN)

# Cargar analizador de sentimiento
analizador_sentimiento = cargar_analizador_sentimiento()

# Cargar dataset
DATASET_PATH = "bot_combinado/dataset.json"
def cargar_dataset():
    try:
        with open(DATASET_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error al cargar el dataset: {e}")
        return []

dataset = cargar_dataset()

# Handlers de módulos

# Voz transcripción y respuesta
@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    handle_voice(bot, message, dataset, analizador_sentimiento)

# Analisis de links
@bot.message_handler(func=lambda msg: msg.text and "http" in msg.text)
def handle_link_message(message):
    handle_link(bot, message)

# Analisis de imágenes
@bot.message_handler(content_types=['photo'])
def manejar_foto_handler(message):
    manejar_foto(bot, message, cliente_groq)

# Comandos /start y /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.reply_to(
        message,
        "¡Hola! Soy un Ciberbot IA\n"
        "Mi función es informarte acerca de los riesgos digitales:\n"
        "• Puedes enviarme audios y los entenderé para darte una respuesta.\n" 
        "• Analizo enlaces por vos y te confirmo si son maliciosos o no ¡Sólo tenes que enviarme el link URL!.\n" 
        "• Analizo tus capturas de pantalla de correos para detectar si es phishing o no por vos ¡Sólo debes enviarme tu Screenshot!\n"
        "• Soy un glosario de Ciberseguridad, preguntarme algo usando ¿Qué es...? y te explicaré su definición, un ejemplo y cómo prevenirlo.\n",
        parse_mode="Markdown"
    )

# Texto general (Ciberseguridad + Groq)
@bot.message_handler(func=lambda message: message.text and "http" not in message.text)
def responder(message):
    pregunta = message.text

    # 1. Analizar sentimiento
    sentimiento, confianza = analizar_texto(pregunta)
    frase_empatica = ""

    # Si detectamos emoción negativa ( el umbral en 0.6 para una detección más sensible)
    if sentimiento == 'NEG' and confianza > 0.6:
        frase_empatica = "Entiendo tu frustración y lamento que estés pasando por esto. "

   # 2. Buscar en dataset
    respuesta = buscar_en_dataset(pregunta, dataset)
    if respuesta:
        print("Respondiendo desde el dataset.")
        bot.send_chat_action(message.chat.id, 'typing')

        # Analisis de sentimiento + respuesta desde dataset
        respuesta_final = frase_empatica + respuesta
            
        bot.reply_to(message, respuesta_final)
        return

   # 3. Verificar si pertenece a ciberseguridad
    print("No encontrado en dataset, consultando Groq...")
    es_ciber = es_relacionada(pregunta, dataset)
    bot.send_chat_action(message.chat.id, 'typing')

    if es_ciber: # Generar respuesta con groq
        # Analisis de sentimientos + Instrucción de groq
        respuesta_ia = respuesta_groq(pregunta, es_ciber, analizador_sentimiento)
    else:
        # Analisis de sentimiento aunque no sea el tema
        if frase_empatica:
            respuesta_ia = f"{frase_empatica}\nSin embargo, solo puedo responder sobre temas de ciberseguridad."
        else:
            respuesta_ia = "Lo siento, Solo puedo responder sobre temas de ciberseguridad."

    # 3. Responder
    bot.reply_to(message, respuesta_ia)


# Iniciar bot

if __name__ == "__main__":
    print("Bot CiberInfo en ejecución...")
    bot.infinity_polling()
