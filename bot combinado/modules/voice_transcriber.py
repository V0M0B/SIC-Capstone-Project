import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
if not GROQ_API_KEY:
    raise ValueError("No se encuentra el API_KEY de Groq de telegram en su archivo de variables de entorno .env")
groq_client = Groq(api_key=os.getenv(GROQ_API_KEY))

def trascribe_voice_with_groq(bot, message):
    try:
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        temp_file = "temp_voice.ogg"

        with open(temp_file, "wb") as f:
            f.write(downloaded_file)

        with open(temp_file, "rb") as file:
            transcription = groq_client.audio.transcriptions.create(
                file=(temp_file, file.read()),
                model="whisper-large-v3-turbo",
                language="es",
            )

        os.remove(temp_file)
        return transcription.text
    except Exception as e:
        print(f"Error al transcribir: {str(e)}")
        return None

def handle_voice(bot, message):
    bot.send_chat_action(message.chat.id, 'typing')
    text = trascribe_voice_with_groq(bot, message)
    if not text:
        bot.reply_to(message, "❌ No pude transcribir el audio.")
        return
    bot.reply_to(message, f"🎧 Transcripción:\n{text}")