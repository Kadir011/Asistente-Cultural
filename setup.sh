#!/bin/bash

echo "=========================================="
echo "  Setup Asistente Cultural"
echo "=========================================="

# Verificar si PostgreSQL está instalado
echo ""
echo "[1/8] Verificando instalación de PostgreSQL..."
if ! command -v psql &> /dev/null; then
    echo "ERROR: PostgreSQL no está instalado. Por favor, instálalo primero."
    exit 1
fi
echo "PostgreSQL está instalado."

# Valores por defecto
DEFAULT_DB_NAME="asistente_cultural"
DEFAULT_USER="postgres"
DEFAULT_HOST="localhost"
DEFAULT_PORT="5432"

# Pedir información de la base de datos
echo ""
echo "[2/8] Configuración de la base de datos"
echo "--------------------------------------------"

read -p "Nombre de la base de datos (default: $DEFAULT_DB_NAME): " DB_NAME
DB_NAME=${DB_NAME:-$DEFAULT_DB_NAME}

read -p "Usuario de PostgreSQL (default: $DEFAULT_USER): " DB_USER
DB_USER=${DB_USER:-$DEFAULT_USER}

read -p "Host de PostgreSQL (default: $DEFAULT_HOST): " DB_HOST
DB_HOST=${DB_HOST:-$DEFAULT_HOST}

read -p "Puerto de PostgreSQL (default: $DEFAULT_PORT): " DB_PORT
DB_PORT=${DB_PORT:-$DEFAULT_PORT}

read -s -p "Contraseña de PostgreSQL: " DB_PASSWORD
echo ""

export PGPASSWORD="$DB_PASSWORD"

# Verificar conexión a PostgreSQL
echo ""
echo "Verificando conexión a PostgreSQL..."
if ! psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d postgres -c "SELECT 1" &> /dev/null; then
    echo "ERROR: No se pudo conectar a PostgreSQL. Verifica las credenciales."
    exit 1
fi
echo "Conexión exitosa."

# Verificar si la base de datos existe y preguntary si desea recrearla
echo ""
echo "[3/8] Creando/Verificando base de datos..."
EXISTS=$(psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'" 2>/dev/null)

if [ "$EXISTS" = "1" ]; then
    read -p "La base de datos '$DB_NAME' ya existe. ¿Deseas recrearla? (s/n): " RECREATE
    if [ "$RECREATE" = "s" ] || [ "$RECREATE" = "S" ]; then
        echo "Eliminando base de datos existente..."
        psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d postgres -c "DROP DATABASE \"$DB_NAME\"" 2>/dev/null
        echo "Creando nueva base de datos..."
        psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d postgres -c "CREATE DATABASE \"$DB_NAME\""
    else
        echo "Se utilizará la base de datos existente."
    fi
else
    echo "Creando base de datos '$DB_NAME'..."
    psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d postgres -c "CREATE DATABASE \"$DB_NAME\""
fi

# Actualizar settings.py con los datos de la BD
echo ""
echo "[4/8] Actualizando configuración de Django..."

# Verificar si existe .env y crearlo/actualizarlo
ENV_FILE=".env"

# Crear o actualizar el archivo .env con las variables de la base de datos
cat > "$ENV_FILE" << EOF
# Database Configuration
DB_ENGINE=django.db.backends.postgresql
DB_DATABASE=$DB_NAME
DB_USERNAME=$DB_USER
DB_PASSWORD=$DB_PASSWORD
DB_HOST=$DB_HOST
DB_PORT=$DB_PORT
EOF

echo "Configuración de base de datos guardada en $ENV_FILE."

# Verificar si python-dotenv está instalado
python -c "from dotenv import load_dotenv" 2>/dev/null || pip install python-dotenv

# Cargar las variables de entorno
export $(cat "$ENV_FILE" | grep -v '^#' | xargs)

echo "Configuración de base de datos actualizada."

# Instalar dependencias
echo ""
echo "[5/8] Instalando dependencias..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "ADVERTENCIA: No se encontró requirements.txt"
fi

# Crear migraciones
echo ""
echo "[6/8] Creando migraciones..."
python manage.py makemigrations
python manage.py migrate

# Ejecutar populate_data.py
echo ""
echo "[7/8] Ejecutando populate_data.py..."
python manage.py populate_data

# Ejecutar createsuperuser
echo ""
echo "[8/8] Creando superusuario..."
python manage.py createsuperuser

echo ""
echo "=========================================="
echo "  Setup completado exitosamente!"
echo "=========================================="
