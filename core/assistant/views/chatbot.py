import json
from google import genai
from google.genai import types
from django.conf import settings
from django.views import View
from django.http import JsonResponse
from django.contrib.auth import logout
from core.assistant.models import (
    Pais, Temporada, Lugar, Norma, FraseUtil,
    InformacionTour, TipoViajero, TipCultural, Favoritos, Historial
)


# ---------------------------------------------------------------------------
# Cliente Gemini
# ---------------------------------------------------------------------------

def _get_gemini_client():
    """Inicializa el cliente de Gemini AI."""
    return genai.Client(api_key=settings.GEMINI_AI_API_KEY)


# ---------------------------------------------------------------------------
# Contexto del usuario
# ---------------------------------------------------------------------------

def _get_user_context(user):
    """Obtiene contexto del usuario para personalizar respuestas."""
    context_parts = []

    if user and user.is_authenticated:
        context_parts.append(f"Usuario actual: {user.username}")

        historial = (
            Historial.objects
            .filter(usuario=user)
            .select_related('pais', 'tipo_viajero')
            .order_by('-fecha_consulta')[:5]
        )
        paises_visitados = [h.pais.nombre for h in historial if h.pais]
        if paises_visitados:
            context_parts.append(f"Has consultado sobre: {', '.join(paises_visitados)}")

        favoritos_count = Favoritos.objects.filter(usuario=user).count()
        if favoritos_count > 0:
            context_parts.append(f"Tienes {favoritos_count} tips en favoritos")
    else:
        context_parts.append("Usuario no autenticado")

    return " | ".join(context_parts)


# ---------------------------------------------------------------------------
# Búsquedas en base de datos
# ---------------------------------------------------------------------------

def _search_paises(query):
    """Busca países por nombre o código ISO."""
    return (
        Pais.objects.filter(nombre__icontains=query) |
        Pais.objects.filter(codigo_iso__icontains=query)
    )


def _search_lugares(query, pais=None):
    """Busca lugares turísticos."""
    lugares = Lugar.objects.select_related('pais').filter(nombre__icontains=query)
    if pais:
        lugares = lugares.filter(pais=pais)
    return lugares[:10]


def _search_normas(query, pais=None):
    """Busca normas culturales."""
    normas = (
        Norma.objects.select_related('pais').filter(titulo__icontains=query) |
        Norma.objects.select_related('pais').filter(descripcion__icontains=query)
    )
    if pais:
        normas = normas.filter(pais=pais)
    return normas[:10]


def _search_frases(query, pais=None):
    """Busca frases útiles."""
    frases = (
        FraseUtil.objects.select_related('pais').filter(frase_espanol__icontains=query) |
        FraseUtil.objects.select_related('pais').filter(frase_local__icontains=query)
    )
    if pais:
        frases = frases.filter(pais=pais)
    return frases[:10]


def _search_tours(query, pais=None):
    """Busca información de tours."""
    tours = (
        InformacionTour.objects.select_related('pais').filter(titulo__icontains=query) |
        InformacionTour.objects.select_related('pais').filter(descripcion__icontains=query)
    )
    if pais:
        tours = tours.filter(pais=pais)
    return tours[:10]


def _search_tips(query, pais=None, categoria=None, tipo_viajero=None):
    """Busca tips culturales."""
    tips = TipCultural.objects.select_related('pais', 'categoria', 'tipo_viajero').filter(
        contenido__icontains=query
    )
    if pais:
        tips = tips.filter(pais=pais)
    if categoria:
        tips = tips.filter(categoria=categoria)
    if tipo_viajero:
        tips = tips.filter(tipo_viajero=tipo_viajero)
    return tips[:10]


def _get_temporadas(pais):
    """Obtiene las temporadas de un país."""
    return Temporada.objects.filter(pais=pais)


def _get_tipos_viajero():
    """Obtiene todos los tipos de viajero."""
    return TipoViajero.objects.all()


# ---------------------------------------------------------------------------
# Detección de intención
# ---------------------------------------------------------------------------

def _es_pregunta_autenticacion(message_lower):
    """Determina si el mensaje es sobre login/registro/logout."""
    palabras_login = ['login', 'iniciar sesión', 'iniciar sesion', 'entrar', 'loguearme']
    palabras_registro = ['registro', 'registrarme', 'crear cuenta', 'signup', 'register']
    palabras_logout = ['logout', 'cerrar sesión', 'cerrar sesion', 'salir']

    if any(p in message_lower for p in palabras_login):
        return 'login'
    if any(p in message_lower for p in palabras_registro):
        return 'registro'
    if any(p in message_lower for p in palabras_logout):
        return 'logout'
    return None


def _es_pregunta_sobre_pais(message_lower):
    """Determina si el mensaje pregunta sobre un país específico."""
    for pais in Pais.objects.all():
        if pais.nombre.lower() in message_lower or pais.codigo_iso.lower() in message_lower:
            return pais
    return None


def _es_pregunta_favoritos(message_lower):
    palabras = ['favorito', 'guardar', 'guardar en favoritos', 'guardar tip', 'agregar a favoritos']
    return any(p in message_lower for p in palabras)


def _es_pregunta_historial(message_lower):
    palabras = ['historial', 'historia', 'consultas anteriores', 'qué he visto', 'que he visto']
    return any(p in message_lower for p in palabras)


def _es_pregunta_recomendacion(message_lower):
    palabras = ['recomienda', 'recomendación', 'sugiere', 'sugiero', 'qué me recomiendas', 'que me recomiendas']
    return any(p in message_lower for p in palabras)


def _es_pregunta_normas(message_lower):
    palabras = ['norma', 'regla', 'cultura', 'costumbre', 'qué hacer', 'que hacer', 'prohibido', 'evitar']
    return any(p in message_lower for p in palabras)


def _es_pregunta_frases(message_lower):
    palabras = ['frase', 'cómo decir', 'como decir', 'traducir', 'palabra', 'idioma']
    return any(p in message_lower for p in palabras)


def _es_pregunta_lugares(message_lower):
    palabras = ['lugar', 'turístico', 'turistico', 'visitar', 'attraction', 'tour']
    return any(p in message_lower for p in palabras)


def _es_pregunta_temporadas(message_lower):
    palabras = ['cuándo ir', 'cuando ir', 'mejor época', 'mejor epoca', 'temporada', 'clima', 'weather']
    return any(p in message_lower for p in palabras)


def _es_ayuda_general(message_lower):
    palabras = ['ayuda', 'help', 'qué puedes hacer', 'que puedes hacer', 'comandos', 'opciones']
    return any(p in message_lower for p in palabras)


# ---------------------------------------------------------------------------
# Generadores de respuesta
# ---------------------------------------------------------------------------

def _generar_respuesta_autenticacion(tipo, request=None):
    """Genera respuesta para preguntas de autenticación."""
    if tipo == 'login':
        return {
            'type': 'login_prompt',
            'message': 'Para iniciar sesión, por favor proporciona tu nombre de usuario y contraseña. También puedes hacerlo desde la página de login directamente.'
        }
    if tipo == 'registro':
        return {
            'type': 'registro_prompt',
            'message': 'Para crear una cuenta, te redirigiré a la página de registro donde podrás completar tus datos.'
        }
    if tipo == 'logout':
        if request and request.user.is_authenticated:
            logout(request)
            return {
                'type': 'logout_success',
                'message': 'Has cerrado sesión correctamente. ¡Hasta pronto!'
            }
        return {
            'type': 'logout_failed',
            'message': 'No tienes una sesión activa.'
        }


def _generar_respuesta_pais(pais):
    """Genera respuesta con información de un país."""
    info = f"**{pais.nombre}** ({pais.codigo_iso})\n\n"

    if pais.descripcion_corta:
        info += f"{pais.descripcion_corta}\n\n"

    info += "📍 **Información General:**\n"
    if pais.capital:
        info += f"- Capital: {pais.capital}\n"
    if pais.moneda:
        info += f"- Moneda: {pais.moneda}\n"
    if pais.poblacion:
        info += f"- Población: {pais.poblacion:,}\n"
    if pais.superficie:
        info += f"- Superficie: {pais.superficie} km²\n"
    if pais.idioma_oficial:
        info += f"- Idioma oficial: {pais.idioma_oficial.nombre}\n"
    if pais.ubicacion:
        info += f"\n📌 **Ubicación:** {pais.ubicacion}\n"
    if pais.latitud and pais.longitud:
        info += f"\n🗺️ **Coordenadas:** {pais.latitud}, {pais.longitud}\n"

    return {
        'type': 'pais_info',
        'message': info,
        'pais_id': pais.id
    }


def _generar_respuesta_lugares(lugares):
    """Genera respuesta con lugares turísticos."""
    if not lugares:
        return {'type': 'no_results', 'message': 'No encontré lugares turísticos con esos criterios.'}

    info = "🏛️ **Lugares Turísticos:**\n\n"
    for lugar in lugares:
        info += f"**{lugar.nombre}** ({lugar.pais.nombre})\n"
        info += f"📍 Región: {lugar.get_region_display()}\n"
        if lugar.destacado:
            info += "⭐ Destacado\n"
        if lugar.descripcion:
            info += f"{lugar.descripcion[:150]}...\n"
        info += "\n"

    return {'type': 'lugares', 'message': info}


def _generar_respuesta_normas(normas):
    """Genera respuesta con normas culturales."""
    if not normas:
        return {'type': 'no_results', 'message': 'No encontré normas culturales con esos criterios.'}

    iconos = {
        'regla': '✅',
        'precaucion': '⚠️',
        'prohibicion': '❌',
        'recomendacion': '💡',
    }

    info = "📋 **Normas y Costumbres Culturales:**\n\n"
    for norma in normas:
        icono = iconos.get(norma.tipo, '📌')
        info += f"{icono} **{norma.titulo}** ({norma.get_tipo_display()})\n"
        info += f"{norma.descripcion}\n\n"

    return {'type': 'normas', 'message': info}


def _generar_respuesta_frases(frases):
    """Genera respuesta con frases útiles."""
    if not frases:
        return {'type': 'no_results', 'message': 'No encontré frases con esos criterios.'}

    info = "🗣️ **Frases Útiles:**\n\n"
    for frase in frases:
        info += f"🇪🇸 {frase.frase_espanol}\n"
        info += f"🌎 {frase.frase_local}"
        if frase.pronunciacion:
            info += f" ({frase.pronunciacion})"
        info += f"\n📂 Categoría: {frase.categoria}\n\n"

    return {'type': 'frases', 'message': info}


def _generar_respuesta_tours(tours):
    """Genera respuesta con información de tours."""
    if not tours:
        return {'type': 'no_results', 'message': 'No encontré tours con esos criterios.'}

    info = "🎫 **Tours y Experiencias:**\n\n"
    for tour in tours:
        info += f"**{tour.titulo}** ({tour.pais.nombre})\n"
        if tour.duracion:
            info += f"⏱️ Duración: {tour.duracion}\n"
        if tour.idiomas:
            info += f"🌍 Idiomas: {tour.idiomas}\n"
        if tour.precio_desde:
            info += f"💰 Precio desde: ${tour.precio_desde}\n"
        if tour.incluye:
            info += f"✅ Incluye: {tour.incluye}\n"
        info += "\n"

    return {'type': 'tours', 'message': info}


def _generar_respuesta_tips(tips, incluir_guardar=True):
    """Genera respuesta con tips culturales."""
    if not tips:
        return {'type': 'no_results', 'message': 'No encontré tips culturales con esos criterios.'}

    info = "💡 **Tips Culturales:**\n\n"
    for tip in tips:
        if tip.titulo:
            info += f"**{tip.titulo}**\n"
        if tip.categoria:
            info += f"📂 Categoría: {tip.categoria.nombre}\n"
        if tip.pais:
            info += f"🌎 País: {tip.pais.nombre}\n"
        if tip.tipo_viajero:
            info += f"🎒 Tipo de viaje: {tip.tipo_viajero.nombre}\n"
        info += f"{tip.contenido}\n"
        if incluir_guardar:
            info += f"\n💾 ID del tip: {tip.id} (puedes guardarlo en favoritos)\n"
        info += "\n---\n\n"

    return {'type': 'tips', 'message': info}


def _generar_respuesta_temporadas(temporadas):
    """Genera respuesta con información de temporadas."""
    if not temporadas:
        return {'type': 'no_results', 'message': 'No encontré información de temporadas para este país.'}

    info = "🗓️ **Temporadas para Visitar:**\n\n"
    for temp in temporadas:
        info += f"**{temp.nombre}** ({temp.get_tipo_display()})\n"
        info += f"📅 Período: {temp.get_periodo_display()}\n"
        if temp.descripcion:
            info += f"{temp.descripcion}\n"
        info += "\n"

    return {'type': 'temporadas', 'message': info}


def _generar_respuesta_favoritos(user):
    """Genera respuesta con favoritos del usuario."""
    favoritos = Favoritos.objects.filter(usuario=user).select_related(
        'tip', 'tip__pais', 'tip__categoria'
    )

    if not favoritos.exists():
        return {
            'type': 'favoritos_vacios',
            'message': 'No tienes favoritos guardados. ¡Guarda tips que te parezcan interesantes!'
        }

    info = f"⭐ **Tus Favoritos ({favoritos.count()}):**\n\n"
    for fav in favoritos:
        if fav.tip:
            info += f"- {fav.tip.titulo or fav.tip.contenido[:50]}..."
            if fav.tip.pais:
                info += f" ({fav.tip.pais.nombre})"
            info += f"\nGuardado: {fav.fecha_guardado.strftime('%d/%m/%Y')}\n\n"

    return {'type': 'favoritos', 'message': info}


def _generar_respuesta_historial(user):
    """Genera respuesta con historial del usuario."""
    historial = (
        Historial.objects
        .filter(usuario=user)
        .select_related('pais', 'tipo_viajero')
        .order_by('-fecha_consulta')[:10]
    )

    if not historial.exists():
        return {
            'type': 'historial_vacio',
            'message': 'No tienes consultas en tu historial. ¡Explora países y lugares!'
        }

    info = "📜 **Tu Historial de Consultas:**\n\n"
    for h in historial:
        info += f"- {h.pais.nombre if h.pais else 'General'}"
        if h.tipo_viajero:
            info += f" ({h.tipo_viajero.nombre})"
        info += f" - {h.fecha_consulta.strftime('%d/%m/%Y %H:%M')}\n"

    return {'type': 'historial', 'message': info}


def _generar_respuesta_ayuda():
    """Genera mensaje de ayuda general."""
    return {
        'type': 'ayuda',
        'message': """🤖 **Asistente Cultural - Estoy para ayudarte con:**

🌍 **Información de Países:**
- "Dime sobre Ecuador"
- "¿Cuál es la capital de Perú?"

🏛️ **Lugares Turísticos:**
- "Lugares turísticos en Colombia"
- "¿Qué lugares visitar en España?"

📋 **Normas Culturales:**
- "Normas de Japón"
- "¿Qué evitar en Francia?"

🗣️ **Frases Útiles:**
- "Frases básicas en italiano"
- "Cómo decir gracias en japonés"

🗓️ **Temporadas:**
- "¿Cuándo ir a Brasil?"
- "Mejor época para visitar México"

🎫 **Tours:**
- "Tours en Argentina"
- "Experiencias en Perú"

💡 **Tips Culturales:**
- "Tips de comida en Italia"
- "Consejos para viajeros en México"

⭐ **Personal:**
- "Mis favoritos"
- "Mi historial"
- "Recomiéndame un destino"

🔐 **Cuenta:**
- "Iniciar sesión"
- "Cerrar sesión"

¿En qué puedo ayudarte hoy?"""
    }


def _generar_respuesta_recomendacion(message_lower, user):
    """Genera recomendaciones personalizadas."""
    tipos_viajero = _get_tipos_viajero()

    tipo_viajero_encontrado = next(
        (tv for tv in tipos_viajero if tv.nombre.lower() in message_lower),
        None
    )

    tips = TipCultural.objects.select_related('pais', 'categoria', 'tipo_viajero')

    if tipo_viajero_encontrado:
        tips = tips.filter(tipo_viajero=tipo_viajero_encontrado)

    tips = list(tips.filter(destacado=True)[:5])

    if not tips:
        tips = list(TipCultural.objects.select_related('pais', 'categoria', 'tipo_viajero')[:5])

    info = "🌟 **Recomendaciones Personalizadas:**\n\n"

    if tipo_viajero_encontrado:
        info += f"Para viajeros **{tipo_viajero_encontrado.nombre}**:\n\n"

    for tip in tips:
        if tip.titulo:
            info += f"**{tip.titulo}**\n"
        if tip.pais:
            info += f"🌎 {tip.pais.nombre}\n"
        if tip.categoria:
            info += f"📂 {tip.categoria.nombre}\n"
        info += f"{tip.contenido[:100]}...\n\n"

    return {'type': 'recomendaciones', 'message': info}


# ---------------------------------------------------------------------------
# Procesamiento con Gemini (fallback)
# ---------------------------------------------------------------------------

def _procesar_mensaje_con_gemini(user_message, history, context):
    """Procesa el mensaje con Gemini AI como fallback."""
    try:
        client = _get_gemini_client()

        system_prompt = f"""Eres el Asistente Cultural, un guía de viaje amigable y experto en culturas de todo el mundo.
Ayudas a los usuarios a planificar sus viajes proporcionando información sobre países, lugares turísticos,
normas culturales, frases útiles en diferentes idiomas, tips de viaje y recomendaciones personalizadas.

Contexto del usuario: {context}

Instrucciones:
- Sé amable y servicial
- Proporciona información precisa y útil
- Si no tienes datos específicos, sugiere al usuario consultar la base de datos
- Usa emojis para hacer las respuestas más atractivas
- Los comandos disponibles son: países, lugares, normas, frases, tours, tips, favoritos, historial
- Responde siempre en español"""

        messages_for_gemini = [
            types.Content(role="user", parts=[types.Part(text=system_prompt)]),
        ]

        for msg in history[-5:]:
            role = "model" if msg.get("role") == "assistant" else "user"
            messages_for_gemini.append(
                types.Content(role=role, parts=[types.Part(text=msg.get("content", ""))])
            )

        messages_for_gemini.append(
            types.Content(role="user", parts=[types.Part(text=user_message)])
        )

        response = client.models.generate_content(
            model="gemini-3.1-pro-preview",
            contents=messages_for_gemini
        )

        return {'type': 'ai_response', 'message': response.text}

    except Exception as e:
        print(f"[Gemini Error] {e}")
        error_msg = str(e)
        if "API_KEY" in error_msg or "api key" in error_msg.lower():
            return {
                'type': 'error',
                'message': 'Configuración de API incomplete. Por favor contacta al administrador.'
            }
        return {
            'type': 'error',
            'message': f'Lo siento, tuve un problema al procesar tu mensaje. Error: {error_msg[:50]}...'
        }


# ---------------------------------------------------------------------------
# Orquestador principal
# ---------------------------------------------------------------------------

def _buscar_en_base_datos(message_lower, user, request=None):
    """Busca información en la base de datos según el mensaje."""
    pais_encontrado = _es_pregunta_sobre_pais(message_lower)

    if _es_ayuda_general(message_lower):
        return _generar_respuesta_ayuda()

    tipo_auth = _es_pregunta_autenticacion(message_lower)
    if tipo_auth:
        return _generar_respuesta_autenticacion(tipo_auth, request=request)

    if user and user.is_authenticated:
        if _es_pregunta_favoritos(message_lower):
            return _generar_respuesta_favoritos(user)

        if _es_pregunta_historial(message_lower):
            return _generar_respuesta_historial(user)

    if _es_pregunta_recomendacion(message_lower):
        return _generar_respuesta_recomendacion(message_lower, user)

    if pais_encontrado:
        if _es_pregunta_temporadas(message_lower):
            response = _generar_respuesta_temporadas(_get_temporadas(pais_encontrado))
            response['pais'] = pais_encontrado.nombre
            return response

        if _es_pregunta_normas(message_lower):
            return _generar_respuesta_normas(_search_normas('', pais_encontrado))

        if _es_pregunta_frases(message_lower):
            return _generar_respuesta_frases(_search_frases('', pais_encontrado))

        if _es_pregunta_lugares(message_lower) or 'visitar' in message_lower:
            return _generar_respuesta_lugares(_search_lugares('', pais_encontrado))

        if 'tour' in message_lower or 'experiencia' in message_lower:
            return _generar_respuesta_tours(_search_tours('', pais_encontrado))

        return _generar_respuesta_pais(pais_encontrado)

    if _es_pregunta_normas(message_lower):
        query = (
            message_lower
            .replace('normas', '')
            .replace('regla', '')
            .replace('cultura', '')
            .strip()
        )
        normas = _search_normas(query) if query else Norma.objects.all()[:10]
        return _generar_respuesta_normas(normas)

    if _es_pregunta_frases(message_lower):
        query = (
            message_lower
            .replace('frases', '')
            .replace('decir', '')
            .replace('traducir', '')
            .strip()
        )
        frases = _search_frases(query) if query else FraseUtil.objects.all()[:10]
        return _generar_respuesta_frases(frases)

    if _es_pregunta_lugares(message_lower):
        query = (
            message_lower
            .replace('lugares', '')
            .replace('turístico', '')
            .replace('turistico', '')
            .replace('visitar', '')
            .strip()
        )
        lugares = _search_lugares(query) if query else Lugar.objects.all()[:10]
        return _generar_respuesta_lugares(lugares)

    if _es_pregunta_temporadas(message_lower):
        query = (
            message_lower
            .replace('cuándo', '')
            .replace('cuando', '')
            .replace('ir', '')
            .replace('temporada', '')
            .strip()
        )
        pais_temp = _es_pregunta_sobre_pais(query) if query else None
        if pais_temp:
            return _generar_respuesta_temporadas(_get_temporadas(pais_temp))

    if 'tour' in message_lower:
        query = message_lower.replace('tour', '').replace('experiencia', '').strip()
        tours = _search_tours(query) if query else InformacionTour.objects.all()[:10]
        return _generar_respuesta_tours(tours)

    return None


def _guardar_en_historial(user, pais):
    """Guarda la consulta en el historial del usuario."""
    if user and user.is_authenticated and pais:
        Historial.objects.create(usuario=user, pais=pais)


# ---------------------------------------------------------------------------
# Vistas
# ---------------------------------------------------------------------------

class ChatbotCulturalView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "").strip()
            history = data.get("history", [])

            if not user_message:
                return JsonResponse({"error": "Mensaje vacío"}, status=400)

        except Exception as e:
            print(f"[Chatbot ERROR] {e}")
            return JsonResponse({"error": str(e)}, status=500)

        message_lower = user_message.lower()
        user = request.user if request.user.is_authenticated else None

        pais_encontrado = _es_pregunta_sobre_pais(message_lower)
        _guardar_en_historial(user, pais_encontrado)

        db_response = _buscar_en_base_datos(message_lower, user, request=request)

        if db_response:
            return JsonResponse({
                "message": db_response['message'],
                "type": db_response['type'],
                "pais_id": db_response.get('pais_id'),
                "pais": db_response.get('pais'),
            })

        context = _get_user_context(user)
        ai_response = _procesar_mensaje_con_gemini(user_message, history, context)

        return JsonResponse({
            "message": ai_response['message'],
            "type": ai_response['type'],
        })

    def get(self, request):
        return JsonResponse({
            "message": "¡Hola! Soy tu Asistente Cultural. ¿En qué puedo ayudarte hoy?",
            "type": "saludo",
        })


class ChatbotGuardarFavoritoView(View):
    """Endpoint para guardar un tip en favoritos."""

    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse(
                {"error": "Debes iniciar sesión para guardar favoritos"}, status=401
            )

        try:
            data = json.loads(request.body)
            tip_id = data.get("tip_id")

            if not tip_id:
                return JsonResponse({"error": "ID del tip no proporcionado"}, status=400)

            tip = TipCultural.objects.get(id=tip_id)
            favorito, created = Favoritos.objects.get_or_create(
                usuario=request.user, tip=tip
            )

            if created:
                return JsonResponse({
                    "message": "✅ Tip guardado en favoritos",
                    "type": "favorito_guardado",
                })
            return JsonResponse({
                "message": "ℹ️ Este tip ya está en tus favoritos",
                "type": "favorito_existente",
            })

        except TipCultural.DoesNotExist:
            return JsonResponse({"error": "Tip no encontrado"}, status=404)
        except Exception as e:
            print(f"[Favorito ERROR] {e}")
            return JsonResponse({"error": str(e)}, status=500)


class ChatbotQuitarFavoritoView(View):
    """Endpoint para quitar un tip de favoritos."""

    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse(
                {"error": "Debes iniciar sesión para quitar favoritos"}, status=401
            )

        try:
            data = json.loads(request.body)
            tip_id = data.get("tip_id")

            if not tip_id:
                return JsonResponse({"error": "ID del tip no proporcionado"}, status=400)

            eliminado = Favoritos.objects.filter(
                usuario=request.user, tip_id=tip_id
            ).delete()[0]

            if eliminado:
                return JsonResponse({
                    "message": "✅ Tip eliminado de favoritos",
                    "type": "favorito_eliminado",
                })
            return JsonResponse({
                "message": "ℹ️ Este tip no estaba en tus favoritos",
                "type": "favorito_no_existente",
            })

        except Exception as e:
            print(f"[Favorito ERROR] {e}")
            return JsonResponse({"error": str(e)}, status=500)


class ChatbotBuscarView(View):
    """Endpoint para búsqueda directa de países/lugares/tips."""

    def get(self, request):
        query = request.GET.get("q", "").strip()
        tipo = request.GET.get("tipo", "pais")

        if not query:
            return JsonResponse({"error": "Query no proporcionado"}, status=400)

        if tipo == "pais":
            results = [
                {"id": p.id, "nombre": p.nombre, "codigo_iso": p.codigo_iso, "descripcion": p.descripcion_corta}
                for p in _search_paises(query)[:5]
            ]
            return JsonResponse({"results": results})

        if tipo == "lugar":
            results = [
                {"id": l.id, "nombre": l.nombre, "pais": l.pais.nombre, "region": l.get_region_display()}
                for l in _search_lugares(query)[:5]
            ]
            return JsonResponse({"results": results})

        if tipo == "tip":
            results = [
                {
                    "id": t.id,
                    "titulo": t.titulo,
                    "contenido": t.contenido[:100],
                    "categoria": t.categoria.nombre if t.categoria else None,
                }
                for t in _search_tips(query)[:5]
            ]
            return JsonResponse({"results": results})

        return JsonResponse({"error": "Tipo de búsqueda no válido"}, status=400) 