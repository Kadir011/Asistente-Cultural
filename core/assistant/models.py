from django.db import models
from config.utils import get_image

class IdiomaOficial(models.Model):
    nombre = models.CharField(max_length=100, 
                              unique=True, 
                              help_text="Nombre del idioma oficial", 
                              blank=False, null=False, 
                              verbose_name="Nombre del idioma oficial")  

    def __str__(self):
        return f'Idioma Oficial: {self.nombre}'
    
    class Meta:
        verbose_name_plural = "Idiomas Oficiales"
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['nombre'], name='idx_nombre_idioma_oficial'),
        ]

class Pais(models.Model):
    # Campos existentes
    idioma_oficial = models.ForeignKey(IdiomaOficial, on_delete=models.CASCADE, related_name='paises', help_text="Idioma oficial del país", blank=True, null=True, verbose_name="Idioma oficial del país")
    nombre = models.CharField(max_length=100, unique=True, help_text="Nombre del país", blank=False, null=False, verbose_name="Nombre del país")  
    codigo_iso = models.CharField(max_length=3, unique=True, help_text="Código ISO del país", blank=False, null=False, verbose_name="Código ISO") 
    ilustracion = models.ImageField(upload_to='paises', blank=True, null=True, verbose_name="Ilustración del país")
    
    descripcion_corta = models.TextField(max_length=300, help_text="Descripción breve del país", blank=True, null=True, verbose_name="Descripción corta")
    descripcion_completa = models.TextField(help_text="Descripción completa del país", blank=True, null=True, verbose_name="Descripción completa")
    ubicacion = models.CharField(max_length=200, help_text="Ubicación específica (ej: Ecuador - Islas Galápagos)", blank=True, null=True, verbose_name="Ubicación")
    latitud = models.DecimalField(max_digits=10, decimal_places=8, help_text="Latitud para Google Maps", blank=True, null=True, verbose_name="Latitud")
    longitud = models.DecimalField(max_digits=11, decimal_places=8, help_text="Longitud para Google Maps", blank=True, null=True, verbose_name="Longitud")
    
    # Información adicional
    capital = models.CharField(max_length=100, help_text="Capital del país", blank=True, null=True, verbose_name="Capital")
    moneda = models.CharField(max_length=50, help_text="Moneda del país", blank=True, null=True, verbose_name="Moneda")
    poblacion = models.IntegerField(help_text="Población aproximada", blank=True, null=True, verbose_name="Población")
    superficie = models.DecimalField(max_digits=10, decimal_places=2, help_text="Superficie en km²", blank=True, null=True, verbose_name="Superficie (km²)")

    def __str__(self):
        return f'Pais: {self.nombre}' 
    
    def get_image_url(self):
        return get_image(self.ilustracion) 
    
    class Meta:
        verbose_name_plural = "Paises"
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['nombre'], name='idx_nombre_pais'),
            models.Index(fields=['codigo_iso'], name='idx_codigo_iso_pais'),
            models.Index(fields=['idioma_oficial'], name='idx_idioma_oficial_pais'),
        ]

class Temporada(models.Model):
    TIPO_CHOICES = [
        ('calida_humeda', 'Cálida y Húmeda'),
        ('fria_seca', 'Fría y Seca'),
        ('primavera', 'Primavera'),
        ('verano', 'Verano'),
        ('otono', 'Otoño'),
        ('invierno', 'Invierno'),
    ]
    
    MESES_CHOICES = [
        (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'),
        (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'),
        (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')
    ]
    
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name='temporadas', verbose_name="País")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name="Tipo de temporada")
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la temporada")
    mes_inicio = models.IntegerField(help_text="Mes de inicio (1-12)", verbose_name="Mes inicio")
    mes_fin = models.IntegerField(help_text="Mes de fin (1-12)", verbose_name="Mes fin")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    
    def get_mes_inicio_display(self):
        """Retorna el nombre del mes de inicio"""
        meses = dict(self.MESES_CHOICES)
        return meses.get(self.mes_inicio, '')
    
    def get_mes_fin_display(self):
        """Retorna el nombre del mes de fin"""
        meses = dict(self.MESES_CHOICES)
        return meses.get(self.mes_fin, '')
    
    def get_periodo_display(self):
        """Retorna el periodo completo formateado"""
        return f"{self.get_mes_inicio_display()} a {self.get_mes_fin_display()}"
    
    def __str__(self):
        return f'{self.pais.nombre} - {self.nombre}'
    
    class Meta:
        verbose_name_plural = "Temporadas"
        ordering = ['pais', 'mes_inicio']

class GaleriaImagen(models.Model):
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name='galeria', verbose_name="País")
    imagen = models.ImageField(upload_to='galeria/', verbose_name="Imagen")
    titulo = models.CharField(max_length=100, blank=True, null=True, verbose_name="Título")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    orden = models.IntegerField(default=0, help_text="Orden de aparición", verbose_name="Orden")
    
    def __str__(self):
        return f'{self.pais.nombre} - {self.titulo or "Imagen"}'
    
    def get_image_url(self):
        return get_image(self.imagen)
    
    class Meta:
        verbose_name_plural = "Galería de Imágenes"
        ordering = ['pais', 'orden']

class Lugar(models.Model):
    REGION_CHOICES = [
        ('costa', 'Costa'),
        ('sierra', 'Sierra'),
        ('amazonia', 'Amazonía'),
        ('galapagos', 'Galápagos'),
        ('norte', 'Norte'),
        ('sur', 'Sur'),
        ('centro', 'Centro'),
        ('este', 'Este'),
        ('oeste', 'Oeste'),
    ]
    
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name='lugares', verbose_name="País")
    nombre = models.CharField(max_length=100, verbose_name="Nombre del lugar")
    region = models.CharField(max_length=20, choices=REGION_CHOICES, verbose_name="Región")
    descripcion = models.TextField(verbose_name="Descripción")
    destacado = models.BooleanField(default=False, help_text="Mostrar como lugar destacado", verbose_name="Destacado")
    imagen = models.ImageField(upload_to='lugares/', blank=True, null=True, verbose_name="Imagen del lugar")
    
    def __str__(self):
        return f'{self.pais.nombre} - {self.nombre}'
    
    def get_image_url(self):
        return get_image(self.imagen)
    
    class Meta:
        verbose_name_plural = "Lugares"
        ordering = ['pais', 'region', 'nombre']

class Norma(models.Model):
    TIPO_CHOICES = [
        ('regla', 'Regla'),
        ('precaucion', 'Precaución'),
        ('prohibicion', 'Prohibición'),
        ('recomendacion', 'Recomendación'),
    ]
    
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name='normas', verbose_name="País")
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, verbose_name="Tipo de norma")
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descripcion = models.TextField(verbose_name="Descripción")
    orden = models.IntegerField(default=0, verbose_name="Orden")
    icono = models.CharField(max_length=50, blank=True, null=True, help_text="Clase CSS del icono (ej: fas fa-passport)", verbose_name="Icono")
    
    def __str__(self):
        return f'{self.pais.nombre} - {self.titulo}'
    
    class Meta:
        verbose_name_plural = "Normas"
        ordering = ['pais', 'tipo', 'orden']

class FraseUtil(models.Model):
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name='frases_utiles', verbose_name="País")
    frase_espanol = models.CharField(max_length=200, verbose_name="Frase en español")
    frase_local = models.CharField(max_length=200, verbose_name="Frase en idioma local")
    pronunciacion = models.CharField(max_length=200, blank=True, null=True, verbose_name="Pronunciación")
    audio = models.FileField(upload_to='audio/', blank=True, null=True, verbose_name="Audio de pronunciación")
    categoria = models.CharField(max_length=50, default='basico', help_text="Categoría de la frase", verbose_name="Categoría")
    
    def __str__(self):
        return f'{self.pais.nombre} - {self.frase_espanol}'
    
    class Meta:
        verbose_name_plural = "Frases Útiles"
        ordering = ['pais', 'categoria']

class InformacionTour(models.Model):
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name='info_tours', verbose_name="País")
    titulo = models.CharField(max_length=100, verbose_name="Título")
    descripcion = models.TextField(verbose_name="Descripción")
    duracion = models.CharField(max_length=100, blank=True, null=True, verbose_name="Duración")
    idiomas = models.CharField(max_length=100, blank=True, null=True, verbose_name="Idiomas disponibles")
    precio_desde = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Precio desde")
    incluye = models.TextField(blank=True, null=True, verbose_name="Qué incluye")
    icono = models.CharField(max_length=50, blank=True, null=True, verbose_name="Icono")
    
    def __str__(self):
        return f'{self.pais.nombre} - {self.titulo}'
    
    class Meta:
        verbose_name_plural = "Información de Tours"
        ordering = ['pais', 'titulo']

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, help_text="Nombre de la categoría", blank=False, null=False, verbose_name="Nombre de la categoría")
    descripcion = models.TextField(help_text="Descripción de la categoría", blank=True, null=True, verbose_name="Descripción de la categoría")
    icono = models.CharField(max_length=50, blank=True, null=True, help_text="Clase CSS del icono", verbose_name="Icono")
    color = models.CharField(max_length=7, default='#f97316', help_text="Color hexadecimal", verbose_name="Color")

    def __str__(self):
        return f'Categoría: {self.nombre}' 

    class Meta:
        verbose_name_plural = "Categorías"
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['nombre'], name='idx_nombre_categoria'),
        ]

class TipoViajero(models.Model):
    nombre = models.CharField(max_length=100, unique=True, help_text="Nombre del tipo de viaje", blank=False, null=False, verbose_name="Nombre del tipo de viaje")
    descripcion = models.TextField(help_text="Descripción del tipo de viaje", blank=True, null=True, verbose_name="Descripción del tipo de viaje")
    icono = models.CharField(max_length=50, blank=True, null=True, help_text="Clase CSS del icono", verbose_name="Icono")

    def __str__(self):
        return f'Tipo de Viajero: {self.nombre}' 
    
    class Meta:
        verbose_name_plural = "Tipos de Viajeros"
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['nombre'], name='idx_nombre_tipo_viajero'),
        ]

class TipCultural(models.Model):
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name='tip_culturals', help_text="País del tip cultural", blank=True, null=True, verbose_name="País del tip cultural")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='tip_culturals', help_text="Categoría del tip cultural", blank=True, null=True, verbose_name="Categoría del tip cultural")
    tipo_viajero = models.ForeignKey(TipoViajero, on_delete=models.CASCADE, related_name='tip_culturals', help_text="Tipo de viaje del tip cultural", blank=True, null=True, verbose_name="Tipo de viaje del tip cultural")
    contenido = models.TextField(help_text="Contenido del tip cultural", blank=False, null=False, verbose_name="Contenido del tip cultural")
    
    # ✅ NUEVOS CAMPOS para tips más detallados
    titulo = models.CharField(max_length=200, blank=True, null=True, verbose_name="Título del tip")
    orden = models.IntegerField(default=0, verbose_name="Orden de aparición")
    destacado = models.BooleanField(default=False, verbose_name="Tip destacado")

    def __str__(self):
        return f'Tip Cultural: {self.titulo or self.contenido[:50]}' 
    
    class Meta:
        verbose_name_plural = "Tips Culturales"
        ordering = ['pais', 'categoria', 'orden']
        indexes = [
            models.Index(fields=['contenido'], name='idx_contenido_tip_cultural'),
            models.Index(fields=['pais'], name='idx_pais_tip_cultural'),
            models.Index(fields=['categoria'], name='idx_categoria_tip_cultural'),
            models.Index(fields=['tipo_viajero'], name='idx_tipo_viajero_tip_cultural'),
        ]

class Favoritos(models.Model):
    usuario = models.ForeignKey('security.User', on_delete=models.CASCADE, related_name='paises_favoritos', help_text="Usuario del pais favorito", blank=True, null=True, verbose_name="Usuario del pais favorito")
    tip = models.ForeignKey(TipCultural, on_delete=models.CASCADE, related_name='paises_favoritos', help_text="Tip cultural del pais favorito", blank=True, null=True, verbose_name="Tip cultural del pais favorito")
    fecha_guardado = models.DateTimeField(auto_now_add=True, help_text="Fecha de guardado del pais favorito", blank=True, null=True, verbose_name="Fecha de guardado del pais favorito") 

    def __str__(self):
        return f'Favoritos: {self.usuario.username} - {self.tip.categoria}' 

    class Meta:
        verbose_name_plural = "Favoritos"
        ordering = ['usuario', 'tip']
        indexes = [
            models.Index(fields=['usuario'], name='idx_usuario_favoritos'),
            models.Index(fields=['tip'], name='idx_tip_favoritos'),
        ]

class Historial(models.Model):
    usuario = models.ForeignKey('security.User', on_delete=models.CASCADE, related_name='paises_historial', help_text="Usuario del pais historial", blank=True, null=True, verbose_name="Usuario del pais historial")
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name='paises_historial', help_text="País del pais historial", blank=True, null=True, verbose_name="País del pais historial")
    tipo_viajero = models.ForeignKey(TipoViajero, on_delete=models.CASCADE, related_name='paises_historial', help_text="Tipo de viaje del pais historial", blank=True, null=True, verbose_name="Tipo de viaje del pais historial") 
    fecha_consulta = models.DateTimeField(auto_now_add=True, help_text="Fecha de consulta del pais historial", blank=True, null=True, verbose_name="Fecha de consulta del pais historial") 

    def __str__(self):
        return f'Historial: {self.usuario.username} - {self.pais}' 

    class Meta:
        verbose_name_plural = "Historial"
        ordering = ['usuario', 'pais']
        indexes = [
            models.Index(fields=['usuario'], name='idx_usuario_historial'),
            models.Index(fields=['pais'], name='idx_pais_historial'),
            models.Index(fields=['tipo_viajero'], name='idx_tipo_viajero_historial'),
        ]


