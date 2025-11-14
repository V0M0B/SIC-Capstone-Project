# 🛡️ Proyecto CiberBot IA: Asistente de Ciberseguridad en Telegram | SIC-Capstone-Project 2025

Este proyecto es un **CiberBot IA** multifuncional desplegado en Telegram. Su objetivo principal es actuar como un **asistente educativo y de prevención** en temas de ciberseguridad, combinando un glosario basado en un dataset, un potente modelo de lenguaje (Groq/LLaMA), y herramientas externas de análisis (voz, enlaces, sentimiento, imágenes).

Es un proyecto ideal que unificamos lo aprendido sobre la integración de múltiples APIs y modelos de IA en un solo sistema con programación en lenguaje Python durante el **programa de Samsung Innovation Campus con el Instructor Alejandro Sosa.**

👩‍💻 **Coders del proyecto:**
- *Sara Giangiacomo*
- *Victoria Bellorin*
- *Lisseidi Nuñez*

## 📋 Tabla de Contenidos
- [🎯 Objetivo del Proyecto](#-objetivo-del-proyecto)
- [✨ Funcionalidades Clave del CiberBot](#-funcionalidades-clave-del-ciberbot)
- [🧠 Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [🔧 Requisitos Previos y Configuración](#-requisitos-previos-y-configuración)
- [🚀 Estructura del Proyecto y Flujo de Lógica](#-estructura-del-proyecto-y-flujo-de-lógica)
- [🎨 Personalización y Próximos Pasos](#-personalización-y-próximos-pasos)

---

## 🎯 Objetivo del Proyecto

El **CiberBot IA** busca ser una herramienta de concientización y respuesta rápida en ciberseguridad. Proporciona:

1.  **Respuestas Inmediatas:** Utiliza un glosario (`dataset.json`) para definir rápidamente conceptos como *Phishing*, *Malware* o *Ransomware*, etc.
2.  **Información Contextual:** Emplea un modelo avanzado (Groq/LLaMA 3.1) para responder preguntas complejas que no están en el glosario, manteniendo la restricción temática.
3.  **Prevención Activa:** Analiza enlaces sospechosos (anti-phishing) y facilita la interacción mediante voz.
4.  **Respuesta Empática:** Usa análisis de sentimiento (Transformers) para ajustar el tono de la respuesta si detecta que el usuario está molesto o preocupado.

---

## ✨ Funcionalidades Clave del CiberBot

El bot responde a diferentes tipos de mensajes mediante módulos especializados, como se muestra en los archivos `main.py` y `logica.py`:

| Tipo de Interacción | Módulo / Función | Descripción |

| **Pregunta de Texto** | `logica.py` + `dataset.json` + `respuesta_groq` | *Prioriza* la búsqueda en el glosario. Si no encuentra, usa **Groq** (`llama-3.1-8b-instant`) para generar una respuesta especializada. |
| **Mensaje de Voz** | `voice_transcriber.py` (Groq Whisper) | Transcribe el audio del usuario a texto y luego procesa la transcripción como una pregunta de texto (buscando en el dataset o en Groq). |
| **Envío de un Enlace (URL)** | `link_checker.py` (Google WebRisk API) | Analiza la URL para detectar amenazas como *Malware*, *Ingeniería Social* o *Software no deseado*. **Recomienda al usuario si es seguro o no.** y **Guía denuncia en Argentina**|
| **Análisis de Sentimiento** | `sentiment_analyzer.py` (Hugging Face Transformers) | Antes de enviar a Groq, analiza el sentimiento del usuario. Si es **NEGATIVO** o de preocupación, ajusta el *prompt* para que la respuesta sea más **empática y calmada**. |

---

## 🧠 Tecnologías Utilizadas

| Componente | Tecnología/Biblioteca | Propósito |

| **Plataforma del Bot** | `python-telegram-bot` (telebot) | Manejo de comandos y mensajes de Telegram. |
| **Glosario y Lógica** | Python (`logica.py`), `difflib.SequenceMatcher` | Almacenamiento de FAQs y lógica de búsqueda por similitud (`dataset.json`). |
| **IA Principal (Generación de Texto)** | **Groq API** (`llama-3.1-8b-instant`) | Generación de respuestas avanzadas de ciberseguridad. |
| **Transcripción de Voz** | **Groq API** (`whisper-large-v3-turbo`) | Conversión de archivos de audio (OGG) a texto. |
| **Análisis de Sentimiento** | **Hugging Face Transformers** (`pysentimiento/robertuito-sentiment-analysis`) | Evaluación del tono emocional del usuario en español. |
| **Chequeo de URL** | **Google Cloud Web Risk API** | Verificación de enlaces contra bases de datos de amenazas. |
| **Entorno** | `dotenv` | Gestión de variables de entorno y tokens de API. |

---

## 🔧 Requisitos Previos y Configuración

Necesitas obtener y configurar las siguientes claves de API:

1.  **Token de Telegram:** Crea un bot con **BotFather** y obtén el `TELEGRAM_TOKEN`.
2.  **API Key de Groq:** Regístrate y obtén la clave `GROQ_API_KEY`.
3.  **Google Web Risk API:** (Requiere configuración de Google Cloud) para el chequeo de URLs.

### 1. Instalación de Dependencias

```bash
# Crear el entorno virtual
python -m venv venv

# Activar el entorno (ej. Linux/Mac)
source venv/bin/activate

# Instalar las dependencias (asegúrate de incluir todas las bibliotecas necesarias: telebot, groq, requests, transformers, python-dotenv, google-cloud-webrisk)
pip install -r requirements.txt

 2. Configuración de Variables de Entorno 

#Crea un archivo llamado .env en la raíz del proyecto y añade tus claves:
# Archivo .env
TELEGRAM_TOKEN="TU_TOKEN_DE_TELEGRAM_AQUI"
GROQ_API_KEY="TU_API_KEY_DE_GROQ_AQUI"
# Otras variables de entorno necesarias para la API de Google Web Risk (si aplica)

``` 3. Ejecución
# Asegúrate de que tu entorno virtual esté activado
python main.py

---

🚀 Estructura del Proyecto y Flujo de Lógica

#El corazón del bot se encuentra en main.py y el módulo logica.py.

| A. Archivos Clave |
● `main.py: Inicializa el bot y dirige el flujo de mensajes.
● `dataset.json: Glosario de ciberseguridad.
● `modules/logica.py: Contiene la lógica central (búsqueda en dataset y la llamada a Groq con restricción temática).
● `modules/voice_transcriber.py: Maneja la descarga y transcripción de audios.
● `modules/link_checker.py: Implementa el chequeo de URL con Google WebRisk.
● `modules/sentiment_analyzer.py: Carga y usa el modelo de Hugging Face para el análisis de sentimiento.

| B. Flujo de Respuesta de Texto (main.py: responder(message)) |
#Este es el proceso por el que pasa cada mensaje de texto:

1. Búsqueda Rápida en Dataset (Glosario):
    - Se llama a buscar_en_dataset(pregunta, dataset) en logica.py.
    - Si encuentra una alta similitud (ej: 0.85), responde con la definición del glosario (dataset.json) y finaliza.

2. Verificación Temática (Ciberseguridad):
    - Si no hay coincidencia en el dataset, se llama a es_relacionada() para determinar si la pregunta es de ciberseguridad.

3. Análisis de Sentimiento:
    - Se llama a analizar_texto() en sentiment_analyzer.py para detectar el estado emocional del usuario (ej: NEG, POS).

4. Llamada a Groq (IA Avanzada):
    - Se llama a respuesta_groq() en logica.py. El prompt del sistema incluye la restricción temática y una instrucción para ser empático si el sentimiento es negativo.
   - Si la pregunta NO es de ciberseguridad, la función está diseñada para devolver el mensaje de restricción: "Solo puedo responder sobre temas de ciberseguridad."


---