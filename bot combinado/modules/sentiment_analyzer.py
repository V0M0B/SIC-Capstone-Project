# Módulo: Análisis de Sentimiento

# Importo la función 'pipeline' de la biblioteca transformers
from transformers import pipeline

# Creo una variable global para el modelo
analizador_sentimiento = None

def cargar_analizador_sentimiento():
    """
    Carga el modelo de análisis de sentimiento y lo deja disponible globalmente.
    Si ocurre un error, devuelve None y el bot puede continuar sin esta función.
    """
    global analizador_sentimiento
    try:
        print("Cargando el modelo de análisis de sentimiento...")
        analizador_sentimiento = pipeline(
            "sentiment-analysis",
            model="pysentimiento/robertuito-sentiment-analysis"
            # model="nlptown/bert-base-multilingual-uncased-sentiment"
        )
        print("¡Modelo cargado con éxito!")
        return analizador_sentimiento
    except Exception as e:
        print(f"Error al cargar el modelo de sentimiento: {e}")
        print("El bot seguirá funcionando sin análisis de sentimiento.")
        return None


def analizar_texto(texto):
    """
    Analiza el sentimiento de un texto y devuelve una tupla (sentimiento, confianza).
    Si no hay modelo disponible, devuelve ('NEU', 0.0).
    """
    global analizador_sentimiento
    if not analizador_sentimiento:
        return "NEU", 0.0
    try:
        resultado = analizador_sentimiento(texto)[0]
        sentimiento = resultado.get('label', 'NEU')
        confianza = resultado.get('score', 0)
        return sentimiento, confianza
    except Exception as e:
        print(f"Error durante el análisis de sentimiento: {e}")
        return "NEU", 0.0
