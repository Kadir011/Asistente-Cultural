import os
import django
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decimal import Decimal
import random

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Importar los modelos - ajustado para apps/assistants/
from core.assistant.models import (
    IdiomaOficial, Pais, Temporada, GaleriaImagen, Lugar, Norma, 
    FraseUtil, InformacionTour, Categoria, TipoViajero, TipCultural, 
    Favoritos, Historial
)

User = get_user_model()

class Command(BaseCommand):
    help = 'Poblar la base de datos con datos de ejemplo para turismo'

    def handle(self, *args, **options):
        self.stdout.write('Creando datos de ejemplo...')
        
        # 1. Crear idiomas oficiales
        idiomas_data = [
            'Español', 'Inglés', 'Francés', 'Portugués', 'Italiano', 
            'Alemán', 'Quechua', 'Guaraní', 'Holandés', 'Japonés'
        ]
        
        idiomas = []
        for nombre in idiomas_data:
            idioma, created = IdiomaOficial.objects.get_or_create(nombre=nombre)
            idiomas.append(idioma)
            if created:
                self.stdout.write(f'✓ Idioma creado: {nombre}')

        # 2. Crear países
        paises_data = [
            {
                'nombre': 'Ecuador',
                'codigo_iso': 'ECU',
                'idioma_oficial': idiomas[0],  # Español
                'capital': 'Quito',
                'moneda': 'Dólar americano',
                'poblacion': 17643054,
                'superficie': Decimal('283561.00'),
                'descripcion_corta': 'País megadiverso ubicado en la línea ecuatorial, hogar de las Islas Galápagos.',
                'descripcion_completa': 'Ecuador es un país sudamericano conocido por su increíble biodiversidad, desde la selva amazónica hasta las islas Galápagos. Ofrece experiencias únicas como el avistamiento de tortugas gigantes, el trekking en los Andes y la exploración de culturas indígenas ancestrales.',
                'ubicacion': 'Sudamérica - Costa del Pacífico',
                'latitud': Decimal('-1.83124000'),
                'longitud': Decimal('-78.18340000')
            },
            {
                'nombre': 'Perú',
                'codigo_iso': 'PER',
                'idioma_oficial': idiomas[0],  # Español
                'capital': 'Lima',
                'moneda': 'Sol peruano',
                'poblacion': 33050325,
                'superficie': Decimal('1285216.00'),
                'descripcion_corta': 'Cuna del Imperio Inca y hogar de Machu Picchu, una de las maravillas del mundo.',
                'descripcion_completa': 'Perú combina historia milenaria con paisajes espectaculares. Desde las ruinas de Machu Picchu hasta la gastronomía de clase mundial, ofrece experiencias culturales y naturales incomparables.',
                'ubicacion': 'Sudamérica - Costa del Pacífico',
                'latitud': Decimal('-9.18997000'),
                'longitud': Decimal('-75.01515000')
            },
            {
                'nombre': 'Colombia',
                'codigo_iso': 'COL',
                'idioma_oficial': idiomas[0],  # Español
                'capital': 'Bogotá',
                'moneda': 'Peso colombiano',
                'poblacion': 51874024,
                'superficie': Decimal('1141748.00'),
                'descripcion_corta': 'Tierra de café, salsa y paisajes que van desde el Caribe hasta la Amazonía.',
                'descripcion_completa': 'Colombia es un país de contrastes que ofrece playas caribeñas, ciudades coloniales, selvas tropicales y la cordillera de los Andes. Su cultura vibrante y hospitalidad hacen de cada visita una experiencia memorable.',
                'ubicacion': 'Sudamérica - Norte',
                'latitud': Decimal('4.57070800'),
                'longitud': Decimal('-74.29733300')
            },
            {
                'nombre': 'Brasil',
                'codigo_iso': 'BRA',
                'idioma_oficial': idiomas[3],  # Portugués
                'capital': 'Brasília',
                'moneda': 'Real brasileño',
                'poblacion': 215313498,
                'superficie': Decimal('8514877.00'),
                'descripcion_corta': 'El país más grande de Sudamérica, famoso por el Carnaval de Río y la selva amazónica.',
                'descripcion_completa': 'Brasil es una nación vibrante que combina playas paradisíacas, la selva amazónica más grande del mundo, ciudades cosmopolitas y una cultura rica en música, danza y festivales.',
                'ubicacion': 'Sudamérica - Este',
                'latitud': Decimal('-14.23500000'),
                'longitud': Decimal('-51.92528000')
            },
            {
                'nombre': 'Argentina',
                'codigo_iso': 'ARG',
                'idioma_oficial': idiomas[0],  # Español
                'capital': 'Buenos Aires',
                'moneda': 'Peso argentino',
                'poblacion': 45605826,
                'superficie': Decimal('2780400.00'),
                'descripcion_corta': 'Tierra del tango, los glaciares patagónicos y la mejor carne del mundo.',
                'descripcion_completa': 'Argentina ofrece desde la elegancia de Buenos Aires hasta los paisajes épicos de la Patagonia. Es el destino perfecto para los amantes del vino, la carne y los deportes de aventura.',
                'ubicacion': 'Sudamérica - Sur',
                'latitud': Decimal('-38.41610000'),
                'longitud': Decimal('-63.61667000')
            }
        ]

        paises = []
        for pais_data in paises_data:
            pais, created = Pais.objects.get_or_create(
                nombre=pais_data['nombre'],
                defaults=pais_data
            )
            paises.append(pais)
            if created:
                self.stdout.write(f'✓ País creado: {pais_data["nombre"]}')

        # 3. Crear temporadas
        temporadas_data = [
            # Ecuador
            {'pais': paises[0], 'tipo': 'fria_seca', 'nombre': 'Temporada Seca', 'mes_inicio': 6, 'mes_fin': 9, 'descripcion': 'Ideal para visitar la sierra y Galápagos'},
            {'pais': paises[0], 'tipo': 'calida_humeda', 'nombre': 'Temporada Húmeda', 'mes_inicio': 10, 'mes_fin': 5, 'descripcion': 'Mejor época para la costa y avistamiento de ballenas'},
            # Perú
            {'pais': paises[1], 'tipo': 'fria_seca', 'nombre': 'Temporada Seca', 'mes_inicio': 5, 'mes_fin': 9, 'descripcion': 'Mejor época para visitar Machu Picchu'},
            {'pais': paises[1], 'tipo': 'calida_humeda', 'nombre': 'Temporada de Lluvias', 'mes_inicio': 10, 'mes_fin': 4, 'descripcion': 'Época de lluvias en los Andes'},
            # Colombia
            {'pais': paises[2], 'tipo': 'fria_seca', 'nombre': 'Temporada Seca', 'mes_inicio': 12, 'mes_fin': 3, 'descripcion': 'Mejor clima para explorar'},
            {'pais': paises[2], 'tipo': 'calida_humeda', 'nombre': 'Temporada Húmeda', 'mes_inicio': 4, 'mes_fin': 11, 'descripcion': 'Temporada de lluvias'},
        ]

        for temp_data in temporadas_data:
            temporada, created = Temporada.objects.get_or_create(**temp_data)
            if created:
                self.stdout.write(f'✓ Temporada creada: {temp_data["nombre"]} - {temp_data["pais"].nombre}')

        # 4. Crear lugares destacados
        lugares_data = [
            # Ecuador
            {'pais': paises[0], 'nombre': 'Islas Galápagos', 'region': 'galapagos', 'destacado': True, 'descripcion': 'Archipiélago único con fauna endémica que inspiró la teoría de la evolución de Darwin.'},
            {'pais': paises[0], 'nombre': 'Centro Histórico de Quito', 'region': 'sierra', 'destacado': True, 'descripcion': 'Patrimonio de la Humanidad con la arquitectura colonial mejor conservada de América.'},
            {'pais': paises[0], 'nombre': 'Baños de Agua Santa', 'region': 'sierra', 'destacado': False, 'descripcion': 'Destino de aventura con aguas termales, cascadas y deportes extremos.'},
            # Perú
            {'pais': paises[1], 'nombre': 'Machu Picchu', 'region': 'sierra', 'destacado': True, 'descripcion': 'Ciudadela inca y una de las nuevas maravillas del mundo moderno.'},
            {'pais': paises[1], 'nombre': 'Valle Sagrado', 'region': 'sierra', 'destacado': True, 'descripcion': 'Valle andino con pueblos tradicionales y sitios arqueológicos incas.'},
            {'pais': paises[1], 'nombre': 'Amazonía Peruana', 'region': 'este', 'destacado': False, 'descripcion': 'Selva tropical con increíble biodiversidad y comunidades nativas.'},
            # Colombia
            {'pais': paises[2], 'nombre': 'Cartagena de Indias', 'region': 'norte', 'destacado': True, 'descripcion': 'Ciudad amurallada colonial con playas caribeñas y vibrante vida nocturna.'},
            {'pais': paises[2], 'nombre': 'Eje Cafetero', 'region': 'centro', 'destacado': True, 'descripcion': 'Región cafetera con paisajes montañosos y haciendas tradicionales.'},
        ]

        for lugar_data in lugares_data:
            lugar, created = Lugar.objects.get_or_create(**lugar_data)
            if created:
                self.stdout.write(f'✓ Lugar creado: {lugar_data["nombre"]}')

        # 5. Crear categorías
        categorias_data = [
            {'nombre': 'Cultura y Tradiciones', 'descripcion': 'Tips sobre costumbres locales, etiqueta social y tradiciones', 'icono': 'fas fa-users', 'color': '#f97316'},
            {'nombre': 'Gastronomía', 'descripcion': 'Información sobre comida típica, restaurantes y hábitos alimenticios', 'icono': 'fas fa-utensils', 'color': '#10b981'},
            {'nombre': 'Transporte', 'descripcion': 'Guías sobre medios de transporte locales y movilidad', 'icono': 'fas fa-bus', 'color': '#3b82f6'},
            {'nombre': 'Alojamiento', 'descripcion': 'Consejos sobre hoteles, hostales y opciones de hospedaje', 'icono': 'fas fa-bed', 'color': '#8b5cf6'},
            {'nombre': 'Seguridad', 'descripcion': 'Recomendaciones de seguridad y precauciones', 'icono': 'fas fa-shield-alt', 'color': '#ef4444'},
            {'nombre': 'Moneda y Compras', 'descripcion': 'Información sobre moneda local, cambio y lugares de compra', 'icono': 'fas fa-shopping-cart', 'color': '#f59e0b'},
            {'nombre': 'Vestimenta', 'descripcion': 'Consejos sobre que vestimenta de cada país se debe conocer.', 'icono': 'fa-solid fa-person-dress', 'color': '#ec4899'},
        ]

        categorias = []
        for cat_data in categorias_data:
            categoria, created = Categoria.objects.get_or_create(
                nombre=cat_data['nombre'],
                defaults=cat_data
            )
            categorias.append(categoria)
            if created:
                self.stdout.write(f'✓ Categoría creada: {cat_data["nombre"]}')

        # 6. Crear tipos de viajero
        tipos_viajero_data = [
            {'nombre': 'Mochilero', 'descripcion': 'Viajeros con presupuesto limitado que buscan experiencias auténticas', 'icono': 'fas fa-hiking'},
            {'nombre': 'Familiar', 'descripcion': 'Familias con niños que buscan destinos seguros y entretenidos', 'icono': 'fas fa-family'},
            {'nombre': 'Aventurero', 'descripcion': 'Viajeros que buscan deportes extremos y experiencias de adrenalina', 'icono': 'fas fa-mountain'},
            {'nombre': 'Cultural', 'descripcion': 'Interesados en historia, arte, museos y patrimonio cultural', 'icono': 'fas fa-university'},
            {'nombre': 'Gastronómico', 'descripcion': 'Viajeros que buscan experiencias culinarias únicas', 'icono': 'fas fa-wine-glass'},
            {'nombre': 'Romántico', 'descripcion': 'Parejas que buscan destinos íntimos y experiencias especiales', 'icono': 'fas fa-heart'},
        ]

        tipos_viajero = []
        for tipo_data in tipos_viajero_data:
            tipo, created = TipoViajero.objects.get_or_create(
                nombre=tipo_data['nombre'],
                defaults=tipo_data
            )
            tipos_viajero.append(tipo)
            if created:
                self.stdout.write(f'✓ Tipo de viajero creado: {tipo_data["nombre"]}')

        # 7. Crear tips culturales
        tips_data = [
            # Ecuador - Tips culturales
            {'pais': paises[0], 'categoria': categorias[0], 'tipo_viajero': tipos_viajero[3], 'titulo': 'Saludo tradicional', 'contenido': 'En Ecuador es común dar la mano al saludar. Entre amigos cercanos se da un beso en la mejilla.', 'destacado': True, 'orden': 1},
            {'pais': paises[0], 'categoria': categorias[0], 'tipo_viajero': tipos_viajero[1], 'titulo': 'Horarios de comida', 'contenido': 'El almuerzo se sirve típicamente entre 12:00 y 14:00, y la cena después de las 19:00.', 'destacado': False, 'orden': 2},
            
            # Ecuador - Gastronomía
            {'pais': paises[0], 'categoria': categorias[1], 'tipo_viajero': tipos_viajero[4], 'titulo': 'Platos típicos', 'contenido': 'No te pierdas el ceviche, la fritada, el locro de papa y el cuy en la sierra.', 'destacado': True, 'orden': 1},
            {'pais': paises[0], 'categoria': categorias[1], 'tipo_viajero': tipos_viajero[0], 'titulo': 'Comida económica', 'contenido': 'Los "almuerzos" (menús del día) en mercados locales cuestan entre $2-4 y son abundantes.', 'destacado': False, 'orden': 2},
            
            # Ecuador - Transporte
            {'pais': paises[0], 'categoria': categorias[2], 'tipo_viajero': tipos_viajero[0], 'titulo': 'Transporte público', 'contenido': 'Los buses urbanos cuestan $0.25. Para distancias largas, las cooperativas de buses son la opción más económica.', 'destacado': False, 'orden': 1},
            {'pais': paises[0], 'categoria': categorias[2], 'tipo_viajero': tipos_viajero[1], 'titulo': 'Taxis y Uber', 'contenido': 'Uber opera en las principales ciudades. Los taxis amarillos oficiales son seguros y usan taxímetro.', 'destacado': False, 'orden': 2},
            
            # Perú - Tips culturales
            {'pais': paises[1], 'categoria': categorias[0], 'tipo_viajero': tipos_viajero[3], 'titulo': 'Respeto por la Pachamama', 'contenido': 'Los pueblos andinos tienen gran respeto por la naturaleza. Participa en ceremonias de ofrenda si te invitan.', 'destacado': True, 'orden': 1},
            {'pais': paises[1], 'categoria': categorias[0], 'tipo_viajero': tipos_viajero[2], 'titulo': 'Mal de altura', 'contenido': 'En ciudades como Cusco (3,400m), toma mate de coca y evita el alcohol los primeros días.', 'destacado': True, 'orden': 2},
            
            # Perú - Gastronomía
            {'pais': paises[1], 'categoria': categorias[1], 'tipo_viajero': tipos_viajero[4], 'titulo': 'Gastronomía mundial', 'contenido': 'Perú es considerado uno de los mejores destinos gastronómicos. Prueba el ceviche, lomo saltado y anticuchos.', 'destacado': True, 'orden': 1},
            {'pais': paises[1], 'categoria': categorias[1], 'tipo_viajero': tipos_viajero[0], 'titulo': 'Mercados locales', 'contenido': 'Los mercados de San Pedro (Cusco) y San Camilo (Arequipa) ofrecen comida auténtica a precios locales.', 'destacado': False, 'orden': 2},
            
            # Colombia - Cultura
            {'pais': paises[2], 'categoria': categorias[0], 'tipo_viajero': tipos_viajero[3], 'titulo': 'Calidez colombiana', 'contenido': 'Los colombianos son muy amables y hospitalarios. No te sorprendas si te invitan a almorzar en casa.', 'destacado': True, 'orden': 1},
            {'pais': paises[2], 'categoria': categorias[0], 'tipo_viajero': tipos_viajero[5], 'titulo': 'Música y baile', 'contenido': 'La salsa, el vallenato y el reggaeton son parte de la cultura. Aprende algunos pasos básicos.', 'destacado': False, 'orden': 2},
            
            # Tips de seguridad
            {'pais': paises[0], 'categoria': categorias[4], 'tipo_viajero': tipos_viajero[0], 'titulo': 'Seguridad en transporte', 'contenido': 'Evita viajar en buses nocturnos en rutas poco transitadas. Prefiere líneas reconocidas.', 'destacado': False, 'orden': 1},
            {'pais': paises[1], 'categoria': categorias[4], 'tipo_viajero': tipos_viajero[1], 'titulo': 'Documentos importantes', 'contenido': 'Lleva siempre una copia de tu pasaporte. El original mantenlo en el hotel.', 'destacado': False, 'orden': 1},
            {'pais': paises[2], 'categoria': categorias[4], 'tipo_viajero': tipos_viajero[2], 'titulo': 'Zonas a evitar', 'contenido': 'Consulta con locales sobre zonas seguras, especialmente para actividades nocturnas.', 'destacado': False, 'orden': 1},
        ]

        for tip_data in tips_data:
            tip, created = TipCultural.objects.get_or_create(**tip_data)
            if created:
                self.stdout.write(f'✓ Tip cultural creado: {tip_data["titulo"]}')

        # 8. Crear normas
        normas_data = [
            # Ecuador
            {'pais': paises[0], 'tipo': 'recomendacion', 'titulo': 'Vacuna contra fiebre amarilla', 'descripcion': 'Recomendada para visitar la región amazónica', 'orden': 1, 'icono': 'fas fa-syringe'},
            {'pais': paises[0], 'tipo': 'regla', 'titulo': 'Entrada a Galápagos', 'descripcion': 'Requiere tarjeta de control de tránsito ($20) y tasa de ingreso ($100-200)', 'orden': 2, 'icono': 'fas fa-passport'},
            {'pais': paises[0], 'tipo': 'prohibicion', 'titulo': 'Productos prohibidos en Galápagos', 'descripcion': 'No se pueden ingresar semillas, plantas o animales', 'orden': 3, 'icono': 'fas fa-ban'},
            
            # Perú
            {'pais': paises[1], 'tipo': 'recomendacion', 'titulo': 'Reserva Machu Picchu', 'descripcion': 'Reserva con 2-3 meses de anticipación, especialmente en temporada alta', 'orden': 1, 'icono': 'fas fa-calendar'},
            {'pais': paises[1], 'tipo': 'regla', 'titulo': 'Documentos requeridos', 'descripcion': 'Pasaporte vigente. Algunos países requieren visa', 'orden': 2, 'icono': 'fas fa-passport'},
            {'pais': paises[1], 'tipo': 'precaucion', 'titulo': 'Altitud', 'descripcion': 'Aclimatarse gradualmente en destinos de altura como Cusco', 'orden': 3, 'icono': 'fas fa-mountain'},
            
            # Colombia
            {'pais': paises[2], 'tipo': 'recomendacion', 'titulo': 'Vacunas recomendadas', 'descripcion': 'Fiebre amarilla para ciertas regiones, hepatitis A y B', 'orden': 1, 'icono': 'fas fa-syringe'},
            {'pais': paises[2], 'tipo': 'precaucion', 'titulo': 'Zonas de precaución', 'descripcion': 'Consultar situación de seguridad en regiones rurales', 'orden': 2, 'icono': 'fas fa-exclamation-triangle'},
        ]

        for norma_data in normas_data:
            norma, created = Norma.objects.get_or_create(**norma_data)
            if created:
                self.stdout.write(f'✓ Norma creada: {norma_data["titulo"]}')

        # 9. Crear frases útiles
        frases_data = [
            # Ecuador
            {'pais': paises[0], 'frase_espanol': 'Hola, ¿cómo está?', 'frase_local': 'Hola, ¿cómo está?', 'pronunciacion': 'O-la, ko-mo es-ta', 'categoria': 'saludo'},
            {'pais': paises[0], 'frase_espanol': '¿Cuánto cuesta?', 'frase_local': '¿Cuánto vale?', 'pronunciacion': 'Kwan-to ba-le', 'categoria': 'compras'},
            {'pais': paises[0], 'frase_espanol': 'Gracias', 'frase_local': 'Gracias', 'pronunciacion': 'Gra-sias', 'categoria': 'cortesia'},
            {'pais': paises[0], 'frase_espanol': '¿Dónde está el baño?', 'frase_local': '¿Dónde queda el baño?', 'pronunciacion': 'Don-de ke-da el ba-ño', 'categoria': 'basico'},
            
            # Perú (con algunas frases en quechua)
            {'pais': paises[1], 'frase_espanol': 'Hola', 'frase_local': 'Rimaykullayki', 'pronunciacion': 'Ri-mai-ku-llai-ki', 'categoria': 'saludo'},
            {'pais': paises[1], 'frase_espanol': 'Gracias', 'frase_local': 'Sulpayki', 'pronunciacion': 'Sul-pai-ki', 'categoria': 'cortesia'},
            {'pais': paises[1], 'frase_espanol': '¿Habla inglés?', 'frase_local': '¿Habla inglés?', 'pronunciacion': 'A-bla in-gles', 'categoria': 'comunicacion'},
            {'pais': paises[1], 'frase_espanol': 'La cuenta, por favor', 'frase_local': 'La cuenta, por favor', 'pronunciacion': 'La kwen-ta por fa-bor', 'categoria': 'restaurante'},
            
            # Colombia
            {'pais': paises[2], 'frase_espanol': '¿Qué tal?', 'frase_local': '¿Qué más?', 'pronunciacion': 'Ke mas', 'categoria': 'saludo'},
            {'pais': paises[2], 'frase_espanol': 'Está muy bueno', 'frase_local': 'Está muy chévere', 'pronunciacion': 'Es-ta mui che-be-re', 'categoria': 'expresion'},
            {'pais': paises[2], 'frase_espanol': 'Disculpe', 'frase_local': 'Perdón', 'pronunciacion': 'Per-don', 'categoria': 'cortesia'},
        ]

        for frase_data in frases_data:
            frase, created = FraseUtil.objects.get_or_create(**frase_data)
            if created:
                self.stdout.write(f'✓ Frase útil creada: {frase_data["frase_espanol"]}')

        # 10. Crear información de tours
        tours_data = [
            # Ecuador
            {'pais': paises[0], 'titulo': 'Tour Galápagos 4 días', 'descripcion': 'Explora las islas con guía naturalista certificado', 'duracion': '4 días / 3 noches', 'idiomas': 'Español, Inglés', 'precio_desde': Decimal('800.00'), 'incluye': 'Transporte, alojamiento, comidas, guía', 'icono': 'fas fa-ship'},
            {'pais': paises[0], 'titulo': 'Aventura en Baños', 'descripcion': 'Deportes extremos y aguas termales', 'duracion': '2 días', 'idiomas': 'Español', 'precio_desde': Decimal('150.00'), 'incluye': 'Actividades, transporte local', 'icono': 'fas fa-mountain'},
            
            # Perú
            {'pais': paises[1], 'titulo': 'Camino Inca a Machu Picchu', 'descripcion': 'Trekking clásico de 4 días', 'duracion': '4 días / 3 noches', 'idiomas': 'Español, Inglés, Quechua', 'precio_desde': Decimal('600.00'), 'incluye': 'Guía, equipo de camping, comidas, permisos', 'icono': 'fas fa-hiking'},
            {'pais': paises[1], 'titulo': 'Tour gastronómico Lima', 'descripcion': 'Descubre la cocina peruana', 'duracion': '1 día', 'idiomas': 'Español, Inglés', 'precio_desde': Decimal('80.00'), 'incluye': 'Degustaciones, guía gastronómico', 'icono': 'fas fa-utensils'},
            
            # Colombia
            {'pais': paises[2], 'titulo': 'Tour del Café', 'descripcion': 'Conoce el proceso del café en fincas tradicionales', 'duracion': '3 días / 2 noches', 'idiomas': 'Español', 'precio_desde': Decimal('200.00'), 'incluye': 'Alojamiento rural, comidas, actividades', 'icono': 'fas fa-coffee'},
            {'pais': paises[2], 'titulo': 'Cartagena Colonial', 'descripcion': 'Tour histórico por la ciudad amurallada', 'duracion': '4 horas', 'idiomas': 'Español, Inglés', 'precio_desde': Decimal('25.00'), 'incluye': 'Guía especializado, entradas', 'icono': 'fas fa-university'},
        ]

        for tour_data in tours_data:
            tour, created = InformacionTour.objects.get_or_create(**tour_data)
            if created:
                self.stdout.write(f'✓ Tour creado: {tour_data["titulo"]}')

        # 11. Crear usuarios de ejemplo (solo si no existen)
        usuarios_data = [
            {'username': 'viajero1', 'email': 'viajero1@example.com', 'first_name': 'Juan', 'last_name': 'Pérez'},
            {'username': 'viajera2', 'email': 'viajera2@example.com', 'first_name': 'María', 'last_name': 'González'},
            {'username': 'aventurero3', 'email': 'aventurero3@example.com', 'first_name': 'Carlos', 'last_name': 'Rodríguez'},
        ]

        usuarios = []
        for user_data in usuarios_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                }
            )
            if created:
                user.set_password('password123')  # Contraseña por defecto
                user.save()
                self.stdout.write(f'✓ Usuario creado: {user_data["username"]}')
            usuarios.append(user)

        # 12. Crear favoritos (algunos usuarios guardan tips)
        if usuarios and TipCultural.objects.exists():
            tips_disponibles = list(TipCultural.objects.all())
            
            favoritos_data = [
                {'usuario': usuarios[0], 'tip': random.choice(tips_disponibles)},
                {'usuario': usuarios[0], 'tip': random.choice(tips_disponibles)},
                {'usuario': usuarios[1], 'tip': random.choice(tips_disponibles)},
                {'usuario': usuarios[1], 'tip': random.choice(tips_disponibles)},
                {'usuario': usuarios[1], 'tip': random.choice(tips_disponibles)},
                {'usuario': usuarios[2], 'tip': random.choice(tips_disponibles)},
            ]

            for fav_data in favoritos_data:
                favorito, created = Favoritos.objects.get_or_create(
                    usuario=fav_data['usuario'],
                    tip=fav_data['tip']
                )
                if created:
                    self.stdout.write(f'✓ Favorito creado: {fav_data["usuario"].username} - {fav_data["tip"].titulo}')

        # 13. Crear historial de consultas
        if usuarios and paises:
            historial_data = [
                {'usuario': usuarios[0], 'pais': paises[0], 'tipo_viajero': tipos_viajero[0]},  # Juan - Ecuador - Mochilero
                {'usuario': usuarios[0], 'pais': paises[1], 'tipo_viajero': tipos_viajero[2]},  # Juan - Perú - Aventurero
                {'usuario': usuarios[1], 'pais': paises[0], 'tipo_viajero': tipos_viajero[1]},  # María - Ecuador - Familiar
                {'usuario': usuarios[1], 'pais': paises[2], 'tipo_viajero': tipos_viajero[3]},  # María - Colombia - Cultural
                {'usuario': usuarios[1], 'pais': paises[1], 'tipo_viajero': tipos_viajero[4]},  # María - Perú - Gastronómico
                {'usuario': usuarios[2], 'pais': paises[2], 'tipo_viajero': tipos_viajero[2]},  # Carlos - Colombia - Aventurero
                {'usuario': usuarios[2], 'pais': paises[0], 'tipo_viajero': tipos_viajero[2]},  # Carlos - Ecuador - Aventurero
            ]

            for hist_data in historial_data:
                historial, created = Historial.objects.get_or_create(**hist_data)
                if created:
                    self.stdout.write(f'✓ Historial creado: {hist_data["usuario"].username} - {hist_data["pais"].nombre}')

        # 14. Crear algunas galerías de imágenes (simuladas)
        galeria_data = [
            # Ecuador
            {'pais': paises[0], 'titulo': 'Tortuga Gigante de Galápagos', 'descripcion': 'Tortuga gigante en su hábitat natural', 'orden': 1},
            {'pais': paises[0], 'titulo': 'Centro Histórico de Quito', 'descripcion': 'Vista panorámica del casco colonial', 'orden': 2},
            {'pais': paises[0], 'titulo': 'Volcán Cotopaxi', 'descripcion': 'El volcán activo más alto del mundo', 'orden': 3},
            {'pais': paises[0], 'titulo': 'Mercado de Otavalo', 'descripcion': 'Textiles tradicionales andinos', 'orden': 4},
            
            # Perú
            {'pais': paises[1], 'titulo': 'Machu Picchu al amanecer', 'descripcion': 'La ciudadela inca con las primeras luces del día', 'orden': 1},
            {'pais': paises[1], 'titulo': 'Lago Titicaca', 'descripcion': 'Islas flotantes de los Uros', 'orden': 2},
            {'pais': paises[1], 'titulo': 'Plaza de Armas - Cusco', 'descripcion': 'Corazón histórico de la antigua capital inca', 'orden': 3},
            {'pais': paises[1], 'titulo': 'Ceviche peruano', 'descripcion': 'Plato bandera de la gastronomía peruana', 'orden': 4},
            
            # Colombia
            {'pais': paises[2], 'titulo': 'Murallas de Cartagena', 'descripcion': 'Fortificaciones coloniales al atardecer', 'orden': 1},
            {'pais': paises[2], 'titulo': 'Plantación de café', 'descripcion': 'Cafetales en el Eje Cafetero', 'orden': 2},
            {'pais': paises[2], 'titulo': 'Playa Rosario', 'descripcion': 'Aguas cristalinas del Caribe colombiano', 'orden': 3},
            {'pais': paises[2], 'titulo': 'Salsa en Cali', 'descripcion': 'Bailarines de salsa en la capital mundial de la salsa', 'orden': 4},
        ]

        for gal_data in galeria_data:
            galeria, created = GaleriaImagen.objects.get_or_create(
                pais=gal_data['pais'],
                titulo=gal_data['titulo'],
                defaults={
                    'descripcion': gal_data['descripcion'],
                    'orden': gal_data['orden']
                }
            )
            if created:
                self.stdout.write(f'✓ Imagen de galería creada: {gal_data["titulo"]}')

        # Resumen final
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('RESUMEN DE DATOS CREADOS:'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(f'✓ Idiomas oficiales: {IdiomaOficial.objects.count()}')
        self.stdout.write(f'✓ Países: {Pais.objects.count()}')
        self.stdout.write(f'✓ Temporadas: {Temporada.objects.count()}')
        self.stdout.write(f'✓ Lugares: {Lugar.objects.count()}')
        self.stdout.write(f'✓ Categorías: {Categoria.objects.count()}')
        self.stdout.write(f'✓ Tipos de viajero: {TipoViajero.objects.count()}')
        self.stdout.write(f'✓ Tips culturales: {TipCultural.objects.count()}')
        self.stdout.write(f'✓ Normas: {Norma.objects.count()}')
        self.stdout.write(f'✓ Frases útiles: {FraseUtil.objects.count()}')
        self.stdout.write(f'✓ Tours: {InformacionTour.objects.count()}')
        self.stdout.write(f'✓ Usuarios: {User.objects.count()}')
        self.stdout.write(f'✓ Favoritos: {Favoritos.objects.count()}')
        self.stdout.write(f'✓ Historial: {Historial.objects.count()}')
        self.stdout.write(f'✓ Galería: {GaleriaImagen.objects.count()}')
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(self.style.SUCCESS('¡Datos creados exitosamente!'))


# Si ejecutas el script directamente (no como comando de Django)
if __name__ == '__main__':
    command = Command()
    command.handle() 



