from google.cloud import webrisk_v1

def check_url_safety(url: str) -> str:
    client = webrisk_v1.WebRiskServiceClient()
    threat_types = [
        webrisk_v1.ThreatType.MALWARE,
        webrisk_v1.ThreatType.SOCIAL_ENGINEERING,
        webrisk_v1.ThreatType.UNWANTED_SOFTWARE,
    ]
    response = client.search_uris(uri=url, threat_types=threat_types)
    if response.threat:
        tipos = [t.name for t in response.threat.threat_types]
        return f"⚠️ Amenaza detectada: {', '.join(tipos)} \n CiberInfo te recomienda no ingresar al enlace ni compartirlo, podés consultar ¿Qué es {', '.join(tipos)}? y te daré una definición de que se trata el riesgo. \n Ingresa a https://www.argentina.gob.ar/servicio/denunciar-un-delito-informatico para saber como realizar una denuncia del delito"
    else:
        return "✅ Enlace seguro.\n Este enlace no figura como denunciado en nuestra base de datos. La confirmación es segura, sin embargo, te recomendamos proseguir con cuidado."

def handle_link(bot, message):
    bot.send_chat_action(message.chat.id, 'typing')
    result = check_url_safety(message.text)
    bot.reply_to(message, result)