import base64
import io
from PIL import Image
import pytesseract
import json
from groq import Groq
import os

#      CARGA DEL DATASET
def cargar_criterios_json(dataset):
    try:
        return dataset.get("deteccionesPhishing", [])
    except:
        return []

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHISHING_JSON_PATH = os.path.join(BASE_DIR, "dataset.json")

try:
    with open(PHISHING_JSON_PATH, "r", encoding="utf-8") as f:
        DATASET = json.load(f)
except:
    DATASET = {}

CRITERIOS_PHISHING = cargar_criterios_json(DATASET)

#        UTILIDAD BASE64
def imagen_a_base64(imagen_bytes):
    return base64.b64encode(imagen_bytes).decode("utf-8")

#    IA DE GROQ — FORMATO BREVE
def describir_imagen_con_groq(cliente_groq, imagen_base64):
    prompt = (
        "Analiza la imagen y responde SOLO lo siguiente:\n"
        "1. ¿Es phishing? responder pero no con si o no\n"
        "2. Explica brevemente en 1 o 2 líneas por qué.\n"
        "No describas colores, logos o elementos visuales. No hagas análisis largos."
    )

    try:
        completado_chat = cliente_groq.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{imagen_base64}"}}
                    ]
                }
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0.3,
            max_tokens=500
        )

        return completado_chat.choices[0].message.content.strip()

    except Exception as e:
        print("Error Groq:", e)
        return None

# BACKUP OCR BREVE
def analizar_phishing(texto_extraido, criterios):
    texto = texto_extraido.lower()
    hallazgos = []

    for c in criterios:
        palabras = c["pregunta"].lower().split()
        if any(p in texto for p in palabras):
            hallazgos.append(c)

    return hallazgos

# MANEJAR FOTO
def manejar_foto(bot, mensaje, cliente_groq):
    try:
        bot.reply_to(mensaje, "📸 Recibí tu imagen. Analizándola...")

        foto = mensaje.photo[-1]
        info = bot.get_file(foto.file_id)
        imagen_bytes = bot.download_file(info.file_path)

        base64_img = imagen_a_base64(imagen_bytes)

        # -------- IA de Groq --------
        respuesta = describir_imagen_con_groq(cliente_groq, base64_img)

        if respuesta:
            # Si detecta phishing, añadimos enlace
            if "sí" in respuesta.lower() or "phishing" in respuesta.lower():
                respuesta += (
                    "\n\n🔗 **Si sospechas que es phishing, denúncialo aquí:**\n"
                    "https://www.gob.mx/profeco/acciones-y-programas/denuncia-tu-caso"
                )
            bot.reply_to(mensaje, respuesta)
            return

        # -------- MODO BACKUP (OCR) --------
        imagen = Image.open(io.BytesIO(imagen_bytes))
        texto = pytesseract.image_to_string(imagen, lang="spa")

        if not texto.strip():
            bot.reply_to(mensaje, "⚠️ No pude analizar la imagen. Intenta de nuevo.")
            return

        hallazgos = analizar_phishing(texto, CRITERIOS_PHISHING)

        if hallazgos:
            r = "⚠️ *Se detectaron señales de phishing mediante OCR:*\n"
            for h in hallazgos:
                r += f"• {h['pregunta']} → {h['respuesta']}\n"

            r += (
                "\n🔗 **Puedes denunciar aquí:**\n"
                "https://www.gob.mx/profeco/acciones-y-programas/denuncia-tu-caso"
            )

            bot.reply_to(mensaje, r, parse_mode="Markdown")
        else:
            bot.reply_to(mensaje, "No detecté textos típicos de phishing.")

    except Exception as e:
        print("Error procesando imagen:", e)
        bot.reply_to(mensaje, "❌ Error al procesar la imagen.")
