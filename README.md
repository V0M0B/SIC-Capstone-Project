# 🛡️ Proyecto CiberBot IA: Asistente de Ciberseguridad en Telegram | SIC-Capstone-Project 2025

Este proyecto es un **CiberBot IA** multifuncional desplegado en Telegram. Su arquitectura combina un potente **Glosario de Ciberseguridad**, la inteligencia de un **Modelo de Lenguaje (LLaMA 3.1 vía Groq)**, y módulos de análisis externo como **Transcripción de Voz**, **Chequeo de Enlaces (Web Risk)**, y **Análisis de Sentimiento**.

Es un proyecto ideal que unifica lo aprendido sobre la integración de múltiples APIs y modelos de IA en un solo sistema con programación en lenguaje **Python** durante el **programa de Samsung Innovation Campus (SIC) con el Instructor Alejandro Sosa.**

---

### 👩‍💻 Coders del proyecto
- *Sara Giangiacomo*
- *Victoria Bellorin*
- *Lisseidi Nuñez*

---

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

1.  **Glosario Rápido:** Utiliza un dataset (`dataset.json`) para definir instantáneamente conceptos clave (*Phishing*, *Malware*, *Ransomware*, etc.).
2.  **Consulta Contextual:** Emplea un modelo avanzado (Groq/LLaMA 3.1) para responder preguntas complejas o contextuales, manteniendo la restricción estricta al tema de ciberseguridad.
3.  **Prevención Activa (Anti-Phishing):** Analiza enlaces y **capturas de pantalla** para prevenir amenazas.
4.  **Interacción Humana:** Permite la comunicación por voz y ajusta el tono de las respuestas gracias al análisis de sentimiento, ofreciendo una **respuesta más empática y calmada** si detecta preocupación o enojo.
5.  **Impacto Social Concreto:** Atiende a una necesidad real, ofreciendo **protección y educación en ciberseguridad** de manera gratuita y accesible para toda la población, de lenguaje entendible para cualquier usuario, demostrando el impacto social directo de la tecnología.

---

## ✨ Funcionalidades Clave del CiberBot

El bot dirige diferentes tipos de mensajes a módulos especializados:

| Tipo de Interacción | Módulo / Función | Descripción |
| :--- | :--- | :--- |
| **Pregunta de Texto** | `logica.py` + `dataset.json` + `respuesta_groq` | **Prioriza** la búsqueda en el glosario. Si no hay coincidencia, usa **Groq** (`llama-3.1-8b-instant`) para generar una respuesta especializada. |
| **Mensaje de Voz** | `voice_transcriber.py` (Groq Whisper) | Transcribe el audio del usuario a texto y luego procesa la transcripción como una pregunta de texto normal. |
| **Envío de un Enlace (URL)** | `link_checker.py` (Google WebRisk API) | Analiza la URL para detectar amenazas. **Recomienda si es seguro/peligroso** e incluye una **Guía de denuncia** específica para Argentina. |
| **Análisis de Imagen (Phishing)** | `image_spam_detector.py` (OCR + Groq Vision) | Analiza capturas de pantalla de correos. Detecta patrones de phishing (logos, urgencia, errores) usando **OCR** y **Groq Vision**. |
| **Análisis de Sentimiento** | `sentiment_analyzer.py` (Hugging Face Transformers) | Evalúa el sentimiento del usuario y ajusta el *prompt* de Groq para una respuesta más **empática**. |

---

## 🧠 Tecnologías Utilizadas

| Componente | Tecnología/Biblioteca | Propósito |
| :--- | :--- | :--- |
| **Plataforma del Bot** | `python-telegram-bot` (telebot) | Manejo de *handlers*, comandos y mensajes de Telegram. |
| **Glosario y Lógica** | Python (`logica.py`), `difflib.SequenceMatcher` | Almacenamiento de FAQs y lógica de búsqueda por similitud (`dataset.json`). |
| **IA Principal (Generación de Texto)** | **Groq API** (`llama-3.1-8b-instant`) | Generación de respuestas avanzadas de ciberseguridad. |
| **Transcripción de Voz** | **Groq API** (`whisper-large-v3-turbo`) | Conversión eficiente de archivos de audio (OGG) a texto. |
| **Análisis de Imagen** | **`pytesseract`** y **Groq Vision** | OCR y análisis de imagen para detección de patrones de phishing. |
| **Análisis de Sentimiento** | **Hugging Face Transformers** (`pysentimiento/robertuito-sentiment-analysis`) | Evaluación del tono emocional del usuario en español. |
| **Chequeo de URL** | **Google Cloud Web Risk API** | Verificación de enlaces contra bases de datos de amenazas. |
| **Entorno** | `dotenv` | Gestión segura de variables de entorno y tokens de API. |

---

## 🔧 Requisitos Previos y Configuración

Necesitas obtener y configurar las siguientes claves de API:

1.  **Token de Telegram:** Crea un bot con **BotFather** y obtén el `TELEGRAM_TOKEN`.
2.  **API Key de Groq:** Regístrate y obtén la clave `GROQ_API_KEY`.
3.  **Google Web Risk API:** (Requiere configuración de Google Cloud) para el chequeo de URLs.

### 💻 Configuración de Google Cloud (CRÍTICO para Web Risk)

Para que la funcionalidad de chequeo de enlaces y análisis de imágenes funcione (ambas utilizan Google Cloud), debes configurar las credenciales en tu entorno local.

1. **Descargar e Instalar `gcloud CLI`:**
    ```bash
    # Descarga e instala el SDK de Google Cloud desde el sitio oficial.
    # Asegúrate de tener Python 3.10+ y que no interfiera con el alias de la Windows Store.
    ```

2. **Autenticación con tu Cuenta de Proyecto (Selecciona una opción):**
    ```bash
    # Opción A: Si la cuenta que quieres usar es la predeterminada en tu navegador
    gcloud auth application-default login

    # Opción B: Si necesitas ingresar con una cuenta específica
    gcloud auth login your_project_account@gmail.com
    gcloud config set account your_project_account@gmail.com
    gcloud auth application-default login
    ```

3. **Crear y Seleccionar el Proyecto (si no existe):**
    ```bash
    # Crea un proyecto (cambia PROJECT_ID por el nombre deseado)
    gcloud projects create PROJECT_ID
    # Configura el CLI para usar ese proyecto
    gcloud config set project PROJECT_ID
    ```

4. **Habilitar APIs Requeridas:**
    ```bash
    # Habilitar Google Web Risk API
    gcloud services enable webrisk.googleapis.com
    ```
    ⚠️ **IMPORTANTE:** Este proyecto utiliza la autenticación **Application Default Credentials (ADC)** de Google. No necesitas poner ninguna clave de Google Cloud en el archivo `.env`.

### 1. Instalación de Dependencias

Se recomienda usar un entorno virtual.

```bash
# Crear el entorno virtual
python -m venv venv

# Activar el entorno (ej. Linux/Mac)
source venv/bin/activate

# Instalar todas las bibliotecas necesarias
pip install -r requirements.txt
2. Configuración de Variables de Entorno
Crea un archivo llamado .env en la raíz del proyecto y añade tus claves.

Bash

# Archivo .env
TELEGRAM_TOKEN="TU_TOKEN_DE_TELEGRAM_AQUI"
GROQ_API_KEY="TU_API_KEY_DE_GROQ_AQUI"
# Otras variables de entorno necesarias para la API de Google Web Risk (NO SE REQUIEREN CLAVES AQUÍ)
3. Ejecución
Bash

# Asegúrate de que tu entorno virtual esté activado
python main.py
Verás el mensaje Bot CiberInfo en ejecución... y el bot comenzará a responder en Telegram.

---

🚀 Estructura del Proyecto y Flujo de Lógica

```
El corazón del bot se encuentra en `main.py y el módulo `logica.py.

A. Archivos Clave
    main.py: Inicializa el bot, carga el modelo de sentimiento, y dirige el flujo de mensajes (texto, voz, links, fotos).
    dataset.json: Contiene el glosario de ciberseguridad y los criterios de detección de Phishing por imagen.
    modules/logica.py: Lógica central (búsqueda en dataset y la llamada a Groq con restricción temática).
    modules/voice_transcriber.py: Maneja la descarga y transcripción de audios con Groq Whisper.
    modules/link_checker.py: Implementa el chequeo de URL con Google WebRisk.
    modules/sentiment_analyzer.py: Carga y usa el modelo de Hugging Face para el análisis de sentimiento.
    modules/image_spam_detector.py: Maneja la descarga, OCR y el análisis de fotos para la detección de Phishing.

B. Flujo de Respuesta de Texto (main.py: responder(message))
 #Este es el proceso por el que pasa cada mensaje de texto:

    Búsqueda Rápida en Dataset (Glosario):
        Se llama a buscar_en_dataset().
        Si encuentra una alta similitud (ej: 0.85), responde con la definición del glosario y finaliza.

    Verificación Temática (Ciberseguridad):
        Si no hay coincidencia, se llama a es_relacionada() para determinar si la pregunta es sobre ciberseguridad.

    Análisis de Sentimiento:
        Se llama a analizar_texto() para detectar el estado emocional.

    Llamada a Groq (IA Avanzada):
        Se llama a respuesta_groq(). El prompt incluye la restricción temática y una instrucción para ser empático.
        Si la pregunta NO es de ciberseguridad, se fuerza la respuesta a: "Solo puedo responder sobre temas de ciberseguridad."

C. Flujo de Análisis de Imagen (main.py: manejar_foto(message))
    #Recepción y Descarga: El handler de fotos en main.py pasa la imagen a image_spam_detector.py.

    Análisis Inicial (OCR + Patrones):
        Se intenta extraer texto de la imagen mediante OCR (pytesseract).
        El texto extraído se compara con los criterios de phishing en dataset.json (Ej: "Logo no coincide", "CTA urgente").
        Si se encuentran patrones, se emite una Alerta de Phishing y Guía de Denuncia.

    Análisis Secundario (Groq Vision/Contexto):
        (Opcional) Si la detección OCR es limitada, se puede enviar la imagen a Groq Vision para un análisis contextual más avanzado.
        Se entrega la respuesta final al usuario.

---