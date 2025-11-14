#BOT COMBINADO (Análisis de imagen, Procesamiento de audio, Análisis de sentimiento, Integración de API URL) + CIBERBOT IA (Groq + Dataset)

#Importaciones base
import telebot as tlb
import os
import requests
import json
import unicodedata
import re
from difflib import SequenceMatcher
from transformers import pipeline
from dotenv import load_dotenv

# Módulos locales
from modules.voice_transcriber import handle_voice
from modules.link_checker import handle_link

# Importamos el nuevo módulo de análisis de sentimiento 
from modules.sentiment_analyzer import cargar_analizador_sentimiento, analizar_texto

# Importamos la lógica general (antes dentro del main)
from modules.logica import (
    buscar_en_dataset, 
    es_relacionada, 
    respuesta_groq
)

# Configuración de entorno y tokens
load_dotenv()

#Configurando entorno de variables
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

if not TELEGRAM_TOKEN:
    raise ValueError("No se encuentra el TOKEN de telegram en su archivo de variables de entorno .env")

# URL de la API de Groq para chat completions (puede cambiar según la documentación de Groq)
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'

# Ruta al archivo JSON que contiene el dataset de preguntas y respuestas
DATASET_PATH = 'dataset.json'

# Crear instancia del bot de Telegram
bot = tlb.TeleBot(TELEGRAM_TOKEN)

# Cargar el analizador de sentimiento desde el módulo
analizador_sentimiento = cargar_analizador_sentimiento()


# Función para cargar el dataset desde el archivo JSON

def cargar_dataset():
    try:
        with open(DATASET_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f" Error al cargar el dataset: {e}")
        return []

dataset = cargar_dataset()

# Handlers de módulos de voz y links

@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    # Pasamos dataset y analizador al módulo de voz
    handle_voice(bot, message, dataset, analizador_sentimiento)


@bot.message_handler(func=lambda msg: msg.text and "http" in msg.text)
def handle_link_message(message):
    handle_link(bot, message)


# Handler/manejador de comandos /start y /help

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

# Handler de texto general (Ciberseguridad + Groq)

@bot.message_handler(func=lambda message: message.text and "http" not in message.text)
def responder(message):
    pregunta = message.text

    # 1. Buscar en dataset
    respuesta = buscar_en_dataset(pregunta, dataset)

    if respuesta:
        print("Respondiendo desde el dataset.")
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message, respuesta)
        return

    # 2. Verificar si pertenece a ciberseguridad
    print("No encontrado en dataset, consultando Groq...")
    es_ciber = es_relacionada(pregunta, dataset)

    bot.send_chat_action(message.chat.id, 'typing')

    if es_ciber:
        # 3. Generar respuesta con Groq
        respuesta_ia = respuesta_groq(pregunta, es_ciber, analizador_sentimiento)
    else:
        respuesta_ia = "Solo puedo responder sobre temas de ciberseguridad."

    # 4. Responder
    bot.reply_to(message, respuesta_ia)


# Iniciar bot
if __name__ == "__main__":
    print(" Bot CiberInfo en ejecución...")
    bot.infinity_polling()
