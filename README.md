<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
<!-- ALL-CONTRIBUTORS-BADGE:END -->
<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)

<br>

# Asistente Cultural

### Tu guía inteligente para explorar el mundo con confianza

<p>
  <strong>Asistente Cultural</strong> es una plataforma web innovadora que combina inteligencia artificial con información cultural detallada para ofrecer a los viajeros una experiencia de viaje más rica y preparada. Desde consejos sobre etiquette local hasta frases útiles en el idioma del país, acompañamos a cada usuario en su descubrimiento cultural.
</p>

[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Development-yellow?style=for-the-badge)]()

---

## Tabla de Contenidos

- [Idea de Negocio](#-idea-de-negocio)
- [Características Principales](#-características-principales)
- [Arquitectura y Tecnologías](#️-arquitectura-y-tecnologías)
- [Instalación Rápida](#-instalación-rápida)
- [ Estructura del Proyecto](#-estructura-del-proyecto)
- [Configuración](#-configuración)
- [Modelos de Datos](#-modelos-de-datos)
- [Chatbot IA](#-chatbot-ia)
- [Contacto](#-contacto)

---

## Idea de Negocio

### El Problema

Los viajeros frecuentemente enfrentan **barreras culturales** que limitan su experiencia:
- Incertidumbre ante normas sociales desconocidas
- Dificultad para comunicarse en idiomás locales
- Información fragmentada y dispersa sobre destinos
- Falta de preparación para situaciones culturales específicas

### Nuestra Solución

**Asistente Cultural** es una plataforma SaaS que proporciona:

| Servicio | Descripción | Valor para el Usuario |
|----------|-------------|----------------------|
| 🤖 Chatbot IA | Consultas personalizadas sobre cultura local | Respuestas instantáneas y contextualizadas |
| 📚 Biblioteca Cultural | Países, lugares, temporadas y normas detalladas | Información estructurada y confiable |
| 💬 Frases Útiles | Expresiones locales con pronunciación | Comunicación efectiva desde el primer día |
| 🎯 Tips Personalizados | Consejos según tipo de viajero | Experiencias adaptadas a cada perfil |
| ❤️ Sistema de Favoritos | Guarda y organiza información | Acceso rápido a contenido relevante |
| 📊 Historial Inteligente | Rastreo de consultas previas | Aprendizaje progresivo del usuario |

### Modelo de Negocio

```
┌─────────────────────────────────────────────────────────────┐
│                    MODELO DE INGRESOS                        │
├─────────────────────────────────────────────────────────────┤
│  Free Tier          │  Premium ($9.99/mes)  │  Enterprise   │
│  ─────────────      │  ──────────────────  │  ──────────    │
│  • 20 consultas/mes  │  • Consultas ilimitadas│  • White-label│
│  • 3 países         │  • Todos los países    │  • Multi-tenant│
│  • Tips básicos     │  • Tips avanzados      │  • Soporte 24/7│
│  • Sin audio        │  • Audio de frases     │  • Personalización│
└─────────────────────────────────────────────────────────────┘
```

### Diferenciadores Competitivos

- **Integración con Gemini AI**: Respuestas inteligentes y contextuales
- **Enfoque Personalizado**: Tips según tipo de viajero (Aventurero, Cultural, Gourmet, etc.)
- **Base de Datos Rica**: Información estructurada y verificable
- **UX Intuitiva**: Interfaz diseñada para facilitar la consulta rápida

---

## Características Principales

### Gestión de Países y Destinos
```
• Información detallada de países (capital, moneda, población, idioma oficial)
• Coordenadas geográficas para integración con mapas
• Descripciones cortas y completas
• Galería de imágenes por país
• Ilustraciones representativas
```

### Lugares y Regiones
```
• Clasificación por regiones (Costa, Sierra, Amazonía, Galápagos, etc.)
• Lugares destacados y su descripción
• Imágenes representativas de cada lugar
```

### Temporadas y Clima
```
• Calendario de temporadas por país
• Meses de inicio y fin para cada temporada
• Descripciones detalladas del clima esperado
```

### Normas Culturales
```
• Reglas de etiqueta y comportamiento
• Precauciones importantes
• Prohibiciones locales
• Recomendaciones de locales
```

### Frases Útiles
```
• Traducciones al idioma local
• Pronunciación fonética
• Audio de pronunciación
• Categorías por contexto (Saludos, Emergencias, Comida, etc.)
```

### Tours e Información
```
• Tours disponibles por país
• Duración, precio e idiomas disponibles
• Qué está incluido en cada tour
```

### Tips Culturales Personalizados
```
• Tips organizados por categoría
• Filtro por tipo de viajero
• Tips destacados y orden personalizado
• Sistema de favoritos para guardar tips
```

### Chatbot con Gemini AI
```
• Consultas en lenguaje natural
• Contexto del país y preferencias del usuario
• Historial de conversaciones
• Respuestas contextualizadas
```

### Sistema de Usuarios
```
• Registro y autenticación
• Perfil de tipo de viajero
• Historial de consultas
• Favoritos personalizados
```

---

## Arquitectura y Tecnologías

### Stack Tecnológico

```
┌──────────────────────────────────────────────────────────────┐
│                        FRONTEND                               │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │   HTML5     │  │   Tailwind   │  │  Alpine.js        │   │
│  │   + CSS3    │  │   CSS        │  │  (Interactivity)   │   │
│  └─────────────┘  └──────────────┘  └────────────────────┘   │
├──────────────────────────────────────────────────────────────┤
│                        BACKEND                                │
│  ┌─────────────────────┐  ┌────────────────────────────────┐│
│  │   Django 5.2        │  │   Django Templates             ││
│  │   (Full Framework)   │  │   (Server-Side Rendering)      ││
│  └─────────────────────┘  └────────────────────────────────┘│
│  ┌─────────────────────┐  ┌────────────────────────────────┐│
│  │   Python 3.10+      │  │   Google Gemini AI             ││
│  │   (Language)        │  │   (Chatbot Engine)             ││
│  └─────────────────────┘  └────────────────────────────────┘│
├──────────────────────────────────────────────────────────────┤
│                        DATA LAYER                            │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │   MySQL     │  │  PostgreSQL  │  │  Django ORM        │   │
│  │   (Dev)     │  │  (Production)│  │  (Abstraction)     │   │
│  └─────────────┘  └──────────────┘  └────────────────────┘   │
├──────────────────────────────────────────────────────────────┤
│                        DEPLOYMENT                             │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │   Local    │  │   Prepared   │  │  Ready for         │   │
│  │  Dev       │  │  for Cloud   │  │  Vercel/Render     │   │
│  └─────────────┘  └──────────────┘  └────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

### Tecnologías Detalladas

| Categoría | Tecnología | Versión | Propósito |
|-----------|-----------|---------|-----------|
| **Framework** | Django | 5.2.4 | Backend completo con ORM |
| **AI** | Google Gemini AI | 1.66.0 | Motor de chatbot inteligente |
| **Frontend** | Tailwind CSS | 3.x | Framework CSS utility-first |
| **Interactivity** | Alpine.js | 3.x | lightweight JavaScript framework |
| **Images** | Pillow | 11.3.0 | Procesamiento de imágenes |
| **Database** | MySQL/PostgreSQL | - | Almacenamiento de datos |
| **Security** | Django Security | - | Autenticación y permisos |

### Patrones de Diseño

```
📐 Patrones Implementados
├── Mixins (Reutilización de lógica de vistas)
├── Generic Views (Vistas basadas en clases)
├── Form Validators (Validación robusta)
├── Model Managers (Consultas optimizadas)
├── Database Indexes (Rendimiento de queries)
└── Context Processors (Variables globales)
```

---

## Instalación Rápida

### Prerrequisitos

```
✅ Python 3.10 o superior
✅ MySQL 8.0 o PostgreSQL 14+
✅ Git
✅ pip (gestor de paquetes Python)
```

### 1. Clonar el Repositorio

```bash
git clone https://github.com/Kadir011/Asistente-Cultural.git
cd Asistente-Cultural
```

### 2. Crear Entorno Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# Configuración de Django
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de Datos (MySQL)
DB_ENGINE=django.db.backends.mysql
DB_NAME=asistente_cultural
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=3306

# Google Gemini API (Opcional - para chatbot)
GOOGLE_API_KEY=tu_api_key_de_gemini
```

### 5. Configurar la Base de Datos

```bash
# Aplicar migraciones
python manage.py migrate

# (Opcional) Cargar datos de ejemplo
python manage.py populate_data

# Crear superusuario para admin
python manage.py createsuperuser
```

### 6. Ejecutar el Servidor

```bash
python manage.py runserver
```

¡Listo! Abre tu navegador en `http://localhost:8000`

---

## Estructura del Proyecto

```
Asistente-Cultural/
│
├── config/                     # Configuración global de Django
│   ├── __init__.py
│   ├── settings.py             # Configuración principal
│   ├── urls.py                 # URLs principales
│   ├── wsgi.py                 # Configuración WSGI
│   ├── asgi.py                 # Configuración ASGI
│   ├── functions.py            # Funciones auxiliares
│   └── utils.py                # Utilidades globales
│
├── core/                       # Aplicación principal
│   ├── __init__.py
│   ├── assistant/              # Módulo de asistente cultural
│   │   ├── __init__.py
│   │   ├── admin.py            # Admin de Django
│   │   ├── apps.py             # Configuración de app
│   │   ├── models.py           # Modelos de datos
│   │   ├── tests.py            # Pruebas unitarias
│   │   ├── urls.py             # URLs del módulo
│   │   ├── views.py            # Vistas principales
│   │   │
│   │   ├── forms/              # Formularios
│   │   │   ├── __init__.py
│   │   │   ├── categoria.py
│   │   │   ├── contacto.py
│   │   │   ├── favoritos.py
│   │   │   ├── frase.py
│   │   │   ├── galeria.py
│   │   │   ├── historial.py
│   │   │   ├── idioma.py
│   │   │   ├── lugar.py
│   │   │   ├── norma.py
│   │   │   ├── pais.py
│   │   │   ├── temporada.py
│   │   │   ├── tip_cultural.py
│   │   │   ├── tipo_viajero.py
│   │   │   └── tour.py
│   │   │
│   │   ├── mixins/             # Mixins reutilizables
│   │   │   ├── __init__.py
│   │   │   └── superuser.py
│   │   │
│   │   ├── views/              # Vistas por funcionalidad
│   │   │   ├── __init__.py
│   │   │   ├── chatbot.py       # Chatbot con Gemini
│   │   │   ├── chat.py
│   │   │   ├── favoritos.py
│   │   │   ├── frase.py
│   │   │   ├── galeria.py
│   │   │   ├── historial.py
│   │   │   ├── home.py
│   │   │   ├── idioma.py
│   │   │   ├── lugar.py
│   │   │   ├── norma.py
│   │   │   ├── pais.py
│   │   │   ├── recomendador.py
│   │   │   ├── temporada.py
│   │   │   ├── tip_cultural.py
│   │   │   ├── tipo_viajero.py
│   │   │   └── tour.py
│   │   │
│   │   └── management/          # Comandos de gestión
│   │       └── commands/
│   │           └── populate_data.py
│   │
│   └── security/               # Módulo de autenticación
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── tests.py
│       ├── urls.py
│       ├── views.py
│       ├── views/
│       │   ├── __init__.py
│       │   └── user.py
│       ├── forms/
│       │   ├── __init__.py
│       │   └── user.py
│       └── urls.py
│
├── media/                      # Archivos subidos por usuarios
├── static/                     # Archivos estáticos (CSS, JS, imágenes)
├── templates/                  # Plantillas HTML
│
├── manage.py                   # Script de gestión Django
├── requirements.txt            # Dependencias Python
├── setup.sh                    # Script de configuración
├── .env                        # Variables de entorno (crear)
├── .gitignore                  # Archivos ignorados por Git
└── README.md                   # Este archivo
```

---

## Configuración

### Panel de Administración

Accede a `http://localhost:8000/admin` con tu superusuario para:

```
📊 Gestión Completa desde Admin
├── 🌐 Países y Destinos
│   ├── Crear, editar, eliminar países
│   ├── Agregar idiomas oficiales
│   ├── Cargar imágenes e ilustraciones
│   └── Gestionar coordenadas GPS
│
├── 📍 Lugares y Regiones
│   ├── CRUD de lugares
│   ├── Clasificación por regiones
│   └── Marcar lugares destacados
│
├── 📅 Temporadas
│   ├── Definir temporadas por país
│   ├── Configurar meses de inicio/fin
│   └── Agregar descripciones
│
├── 📜 Normas Culturales
│   ├── Tipos: Regla, Precaución, Prohibición, Recomendación
│   ├── Organizar por país
│   └── Orden personalizado
│
├── 💬 Frases Útiles
│   ├── Traducciones completas
│   ├── Pronunciación fonética
│   └── Audio (opcional)
│
├── 🎫 Tours e Información
│   ├── Detalles de tours
│   ├── Precios y duraciones
│   └── Idiomas disponibles
│
├── 🎯 Tips Culturales
│   ├── Categorización avanzada
│   ├── Tipos de viajeros
│   ├── Tips destacados
│   └── Orden personalizado
│
├── 👤 Usuarios
│   ├── Perfiles de viajeros
│   ├── Favoritos
│   └── Historial de consultas
│
└── 📊 Dashboard
    ├── Estadísticas generales
    ├── Consultas más populares
    └── Países más visitados
```

### Integración con Google Gemini

Para activar el chatbot IA:

1. Obtén una API key en [Google AI Studio](https://aistudio.google.com/apikey)
2. Agrega la key a tu `.env`: `GOOGLE_API_KEY=tu_key`
3. Reinicia el servidor

El chatbot utilizará Gemini para generar respuestas contextuales basadas en:
- País seleccionado por el usuario
- Tipo de viajero configurado
- Historial de consultas previas
- Base de datos cultural del sistema

---

## Modelos de Datos

### Diagrama de Entidades

```
┌─────────────────┐       ┌─────────────────┐
│  IdiomaOficial  │       │      Pais       │
├─────────────────┤       ├─────────────────┤
│ • nombre         │◄──────│ • nombre        │
└─────────────────┘       │ • codigo_iso    │
                          │ • capital       │
                          │ • moneda        │
                          │ • poblacion     │
                          │ • superficie    │
                          │ • latitud       │
                          │ • longitud      │
                          └────────┬────────┘
                                   │
        ┌───────────────────────────┼───────────────────────────┐
        │           │               │               │           │
        ▼           ▼               ▼               ▼           ▼
┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐
│  Lugares  │ │ Temporadas│ │   Normas  │ │  Frases   │ │   Tours   │
├───────────┤ ├───────────┤ ├───────────┤ ├───────────┤ ├───────────┤
│ • nombre   │ │ • tipo    │ │ • tipo    │ │• frase_es │ │ • titulo  │
│ • region  │ │ • mes_ini │ │ • titulo  │ │• frase_lo │ │ • duracion│
│ • descrip │ │ • mes_fin │ │ • descrip │ │• pronunci │ │ • precio  │
│ • destacado│ └───────────┘ └───────────┘ └───────────┘ └───────────┘
└───────────┘
        │
        ▼
┌───────────┐       ┌───────────┐       ┌──────────────┐
│ Galeria   │       │ TipCult.  │◄──────│   Categoria  │
├───────────┤       ├───────────┤       ├──────────────┤
│ • imagen   │       │ • titulo  │       │ • nombre     │
│ • titulo   │       │ • contenido│      │ • descripcion│
│ • descrip │       │ • destacado│      │ • icono      │
│ • orden    │       │ • orden   │       │ • color      │
└───────────┘       └─────┬─────┘       └──────────────┘
                          │
                          ▼
                  ┌───────────────┐
                  │  TipoViajero  │
                  ├───────────────┤
                  │ • nombre      │
                  │ • descripcion │
                  │ • icono       │
                  └───────┬───────┘
                          │
         ┌────────────────┼────────────────┐
         ▼                                 ▼
  ┌─────────────┐                  ┌─────────────┐
  │  Favoritos  │                  │  Historial  │
  ├─────────────┤                  ├─────────────┤
  │ • usuario   │                  │ • usuario   │
  │ • tip       │                  │ • pais      │
  │ • fecha     │                  │ • tipo_viaj │
  └─────────────┘                  │ • fecha     │
                                   └─────────────┘
```

### Índices de Rendimiento

Cada modelo incluye índices optimizados para consultas rápidas:

```
📈 Índices Configurados
├── Pais: nombre, codigo_iso, idioma_oficial
├── Categoria: nombre
├── TipoViajero: nombre
├── TipCultural: contenido, pais, categoria, tipo_viajero
├── Favoritos: usuario, tip
└── Historial: usuario, pais, tipo_viajero
```

---

## Chatbot IA

### Implementación con Google Gemini

El chatbot está diseñado para proporcionar respuestas culturalmente contextuales:

```python
# core/assistant/views/chatbot.py
# Utiliza Google Gemini AI para generar respuestas inteligentes
# Considerando: país, tipo de viajero, historial, normas culturales
```

### Características del Chatbot

| Función | Descripción |
|---------|-------------|
| **Contexto Cultural** | Utiliza la base de datos del sistema para contexto |
| **Tipo de Viajero** | Adapta respuestas según preferencias del usuario |
| **Historial** | Mantiene contexto de conversaciones anteriores |
| **Fallback** | Respuestas predefinidas si la API no está disponible |
| **Logging** | Registro de todas las consultas para mejora continua |

### Prompt Engineering

El sistema utiliza técnicas de prompt engineering para:
- Mantener tono amigable y respetuoso
- Incluir información verificable de la base de datos
- Sugerir acciones relevantes (tours, frases, tips)
- Personalizar según perfil de viaje

---

## Contacto

<div align="center">

### Kadir Barquet Bravo
**Desarrollador Full Stack | Especializado en Django & AI**

<br>

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Kadir%20Barquet-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/kadir-barquet-bravo/)
[![GitHub](https://img.shields.io/badge/GitHub-Kadir011-333?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Kadir011)
[![Email](https://img.shields.io/badge/Email-barquetbravokadir@gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:barquetbravokadir@gmail.com)

<br>

### ¿Interesado en conectar?

Si te interesa este proyecto, quieres colaborar o discutir oportunidades profesionales, no dudes en contactarme. Estoy abierto a:

```
💼 Oportunidades de empleo como Senior Django Developer
🤝 Proyectos colaborativos de código abierto
💡 Discusiones sobre innovación en turismo y tecnología
🏆 Contributciones a soluciones de IA aplicadas
```

</div>

---

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

<div align="center">

**⭐ Dale una estrella al proyecto si te resultó útil ⭐**

**Hecho con ❤️ y Python 🐍**

</div>
