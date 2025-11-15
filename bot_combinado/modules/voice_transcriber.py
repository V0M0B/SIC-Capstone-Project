import os
from groq import Groq
from dotenv import load_dotenv

# Importamos la lógica central del bot (dataset + ciberseguridad + Groq)
from modules.logica import (
    buscar_en_dataset,
    es_relacionada,
    respuesta_groq
)

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
if not GROQ_API_KEY:
    raise ValueError("No se encuentra el API_KEY de Groq de telegram en su archivo de variables de entorno .env")

# Cliente Groq para transcripción
groq_client = Groq(api_key=GROQ_API_KEY)


# FUNCIÓN DE TRANSCRIPCIÓN

def trascribe_voice_with_groq(bot, message):
    try:
        # Obtener archivo del mensaje de voz
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        temp_file = "temp_voice.ogg"

        # Guardar audio temporalmente
        with open(temp_file, "wb") as f:
            f.write(downloaded_file)

        # Enviar a Whisper para transcripción
        with open(temp_file, "rb") as file:
            transcription = groq_client.audio.transcriptions.create(
                file=(temp_file, file.read()),
                model="whisper-large-v3-turbo",
                language="es",
            )

        # Eliminar archivo temporal
        os.remove(temp_file)

        return transcription.text

    except Exception as e:
        print(f"Error al transcribir: {str(e)}")
        return None


# HANDLER PRINCIPAL PARA AUDIOS

def handle_voice(bot, message, dataset, analizador_sentimiento):
    bot.send_chat_action(message.chat.id, 'typing')

    # 1. Transcribir audio
    text = trascribe_voice_with_groq(bot, message)

    if not text:
        bot.reply_to(message, "Lo siento, no pude transcribir el audio :(")
        return

    # 2. Intentar responder desde el dataset.json
    respuesta_dataset = buscar_en_dataset(text, dataset)

    if respuesta_dataset:
        bot.reply_to(
            message,
            f" *Transcripción:*\n{text}\n\n *Respuesta del glosario:*\n{respuesta_dataset}",
            parse_mode="Markdown"
        )
        return

    # 3. Verificar si la transcripción tiene relación con ciberseguridad
    es_ciber = es_relacionada(text, dataset)

    if not es_ciber:
        bot.reply_to(
            message,
            f" *Transcripción:*\n{text}\n\nSolo puedo responder sobre temas de ciberseguridad.",
            parse_mode="Markdown"
        )
        return

    # 4. Si es de ciberseguridad, generar respuesta con Groq (incluye análisis de sentimiento)
    respuesta_ia = respuesta_groq(text, es_ciber)

    # 5. Enviar respuesta final
    bot.reply_to(
        message,
        f" *Transcripción:*\n{text}\n\n *Respuesta:*\n{respuesta_ia}",
        parse_mode="Markdown"
    )
