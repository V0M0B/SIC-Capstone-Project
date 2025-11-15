import os
import json
import re
import requests
import unicodedata
from difflib import SequenceMatcher
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# API Key y URL para Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


# FUNCIÓN: Buscar coincidencias en el dataset.json

def buscar_en_dataset(pregunta, dataset):
    """
    Busca una pregunta similar dentro del dataset usando similitud
    basada en SequenceMatcher. Devuelve la respuesta encontrada
    o None si no hay coincidencia suficiente.
    """

    try:
        # Normaliza para comparar de forma más precisa
        def normalizar(texto):
            texto = ''.join(
                c for c in unicodedata.normalize('NFD', texto)
                if unicodedata.category(c) != 'Mn'
            )
            texto = texto.lower().strip()
            texto = re.sub(r'\s+', ' ', texto)
            return texto

        # 1. Normalizar la pregunta del usuario 
        pregunta_norm = normalizar(pregunta)
        
        # 2. Preparar variables
        mejor_coincidencia = None
        puntaje_mas_alto = 0.85  # umbral de similitud

        # 3. Acceder a la LISTA correcta del dataset
        lista_de_preguntas = dataset.get("preguntasGenerales", [])

        # 4. Iterar sobre la LISTA 
        for item in lista_de_preguntas:
            similitud = SequenceMatcher(
                None,
                normalizar(item['pregunta']),
                pregunta_norm
            ).ratio()

            # 5. Guardar la mejor coincidencia 
            if similitud > puntaje_mas_alto:
                mejor_coincidencia = item['respuesta']
                puntaje_mas_alto = similitud

        # 6. Devolver el resultado
        return mejor_coincidencia

    except Exception as e:
        print(f"Error en buscar_en_dataset: {e}")
        return None

# FUNCIÓN: Determinar si el mensaje es de ciberseguridad

def es_relacionada(pregunta, dataset):
    """
    Determina si la pregunta tiene relación con temas de ciberseguridad
    buscando palabras clave y comparando contra preguntas del dataset.
    """
    try:
        pregunta_lower = pregunta.lower()
        
        palabras_clave = [
            "ciberseguridad", "phishing", "malware", "ransomware", "spyware",
            "vishing", "smishing", "virus", "troyano", "contraseña", "seguridad",
            "ingeniería social", "hacker", "hacking", "ethical hacking", "hacking ético",
            "ciberacoso", "spam", "suplantación", "spoofing", "identidad", "vpn",
            "redes", "wifi", "huella digital", "fake news", "amenazas", "ciberdelito",
            "robo de identidad", "ataque", "información", "riesgo", "privacidad",
            "firewall", "antivirus", "cifrado", "keylogger", "botnet", "backdoor",
            "rootkit", "clickjacking", "educación digital", "copias de seguridad",
            "gestor de contraseñas", "vulnerabilidad", "zero-day", "seguridad en redes sociales"
        ]

        # Palabras clave directas
        for palabra in palabras_clave:
            if palabra in pregunta_lower:
                return True

        # Comparar con contenido del dataset
        for item in dataset:
            tema = item['pregunta'].lower()
            if any(p in pregunta_lower for p in tema.split() if len(p) > 5):
                return True

        return False

    except Exception as e:
        print(f"Error en es_relacionada: {e}")
        return False



# FUNCIÓN: Llamada a Groq (modelo LLaMA) con restricciones

def respuesta_groq(mensaje, es_tema_ciber, analizador_sentimiento=None):
    """
    Genera una respuesta usando Groq LLaMA.
    Aplica restricciones para que solo responda sobre ciberseguridad.
    Incluye análisis de sentimiento si es provisto.
    """

    sistema_adicional = ""

    # Análisis de sentimiento
    if analizador_sentimiento:
        try:
            resultado = analizador_sentimiento(mensaje)[0]
            sentimiento = resultado.get('label', 'NEU')
            confianza = resultado.get('score', 0)

            if sentimiento == "NEG" and confianza > 0.8:
                sistema_adicional = (
                    "El usuario parece molesto o preocupado. "
                    "Responde con un tono empático, calmado y tranquilizador. "
                )
        except Exception as e:
            print(f"Error durante análisis de sentimiento: {e}")

    # Restricción temática
    restriccion_tema = (
        "Si la pregunta no tiene relación con el tema de ciberseguridad, "
        "o si no está marcada como relevante, responde SOLO con: "
        "'Solo puedo responder sobre temas de ciberseguridad.' "
    )

    headers = {
        'Authorization': f'Bearer {GROQ_API_KEY}',
        'Content-Type': 'application/json'
    }

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": (
                    sistema_adicional +
                    "Eres un asistente especializado en ciberseguridad. "
                    "Solo puedes responder preguntas relacionadas con el contenido del dataset "
                    "(phishing, malware, ransomware, ingeniería social, etc.). "
                    + restriccion_tema +
                    f"La pregunta ha sido pre-analizada como: {'RELEVANTE' if es_tema_ciber else 'NO RELEVANTE'}."
                )
            },
            {"role": "user", "content": mensaje}
        ]
    }

    # Llamada a la API de Groq
    try:
        resp = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=20)

        if resp.status_code == 200:
            return resp.json()['choices'][0]['message']['content'].strip()
        else:
            return f"[Error Groq {resp.status_code}]"

    except Exception as e:
        return f"[Error de conexión a Groq: {e}]"
