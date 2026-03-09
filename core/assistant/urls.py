from django.urls import path
from core.assistant.views import home, pais, categoria, tipo_viajero, temporada, galeria, lugar, norma, frase, tour, tip_cultural, favoritos, historial, recomendador, idioma
 
app_name = 'assistant'

urlpatterns = [
    # ================================
    # RUTAS INICIALES
    # ================================
    path('', home.HomeView.as_view(), name='home'),
    path('about/', home.AboutView.as_view(), name='about'),
    path('contact/', home.ContactView.as_view(), name='contact'),
    path('menu/', home.MenuView.as_view(), name='menu'),

    # ================================
    # RUTAS PÚBLICAS
    # ================================
    path('paises/', pais.PaisListPublicView.as_view(), name='paises_public'),
    path('pais/<int:pk>/', pais.PaisDetailView.as_view(), name='pais_detail'),
    path('recomendaciones/', recomendador.RecommendationView.as_view(), name='recomendaciones'),

    # ================================
    # CRUD IDIOMA OFICIAL
    # ================================
    path('admin/idioma-oficial/', idioma.IdiomaOficialListView.as_view(), name='idioma_oficial_list'),
    path('admin/idioma-oficial/create/', idioma.IdiomaOficialCreateView.as_view(), name='idioma_oficial_create'),
    path('admin/idioma-oficial/<int:pk>/update/', idioma.IdiomaOficialUpdateView.as_view(), name='idioma_oficial_update'),
    path('admin/idioma-oficial/<int:pk>/delete/', idioma.IdiomaOficialDeleteView.as_view(), name='idioma_oficial_delete'),

    # ================================
    # CRUD PAÍS
    # ================================
    path('admin/pais/', pais.PaisListView.as_view(), name='pais_list'),
    path('admin/pais/create/', pais.PaisCreateView.as_view(), name='pais_create'),
    path('admin/pais/<int:pk>/update/', pais.PaisUpdateView.as_view(), name='pais_update'),
    path('admin/pais/<int:pk>/delete/', pais.PaisDeleteView.as_view(), name='pais_delete'),

    # ================================
    # CRUD CATEGORÍA
    # ================================
    path('admin/categoria/', categoria.CategoriaListView.as_view(), name='categoria_list'),
    path('admin/categoria/create/', categoria.CategoriaCreateView.as_view(), name='categoria_create'),
    path('admin/categoria/<int:pk>/update/', categoria.CategoriaUpdateView.as_view(), name='categoria_update'),
    path('admin/categoria/<int:pk>/delete/', categoria.CategoriaDeleteView.as_view(), name='categoria_delete'),

    # ================================
    # CRUD TIPO VIAJERO
    # ================================
    path('admin/tipo-viajero/', tipo_viajero.TipoViajeroListView.as_view(), name='tipo_viajero_list'),
    path('admin/tipo-viajero/create/', tipo_viajero.TipoViajeroCreateView.as_view(), name='tipo_viajero_create'),
    path('admin/tipo-viajero/<int:pk>/update/', tipo_viajero.TipoViajeroUpdateView.as_view(), name='tipo_viajero_update'),
    path('admin/tipo-viajero/<int:pk>/delete/', tipo_viajero.TipoViajeroDeleteView.as_view(), name='tipo_viajero_delete'),

    # ================================
    # CRUD TEMPORADA
    # ================================
    path('admin/temporada/', temporada.TemporadaListView.as_view(), name='temporada_list'),
    path('admin/temporada/create/', temporada.TemporadaCreateView.as_view(), name='temporada_create'),
    path('admin/temporada/<int:pk>/update/', temporada.TemporadaUpdateView.as_view(), name='temporada_update'),
    path('admin/temporada/<int:pk>/delete/', temporada.TemporadaDeleteView.as_view(), name='temporada_delete'),

    # ================================
    # CRUD GALERÍA DE IMÁGENES
    # ================================
    path('admin/galeria-imagen/', galeria.GaleriaImagenListView.as_view(), name='galeria_imagen_list'),
    path('admin/galeria-imagen/create/', galeria.GaleriaImagenCreateView.as_view(), name='galeria_imagen_create'),
    path('admin/galeria-imagen/<int:pk>/update/', galeria.GaleriaImagenUpdateView.as_view(), name='galeria_imagen_update'),
    path('admin/galeria-imagen/<int:pk>/delete/', galeria.GaleriaImagenDeleteView.as_view(), name='galeria_imagen_delete'),

    # ================================
    # CRUD LUGAR
    # ================================
    path('admin/lugar/', lugar.LugarListView.as_view(), name='lugar_list'),
    path('admin/lugar/create/', lugar.LugarCreateView.as_view(), name='lugar_create'),
    path('admin/lugar/<int:pk>/update/', lugar.LugarUpdateView.as_view(), name='lugar_update'),
    path('admin/lugar/<int:pk>/delete/', lugar.LugarDeleteView.as_view(), name='lugar_delete'),

    # ================================
    # CRUD NORMA
    # ================================
    path('admin/norma/', norma.NormaListView.as_view(), name='norma_list'),
    path('admin/norma/create/', norma.NormaCreateView.as_view(), name='norma_create'),
    path('admin/norma/<int:pk>/update/', norma.NormaUpdateView.as_view(), name='norma_update'),
    path('admin/norma/<int:pk>/delete/', norma.NormaDeleteView.as_view(), name='norma_delete'),

    # ================================
    # CRUD FRASE ÚTIL
    # ================================
    path('admin/frase-util/', frase.FraseUtilListView.as_view(), name='frase_util_list'),
    path('admin/frase-util/create/', frase.FraseUtilCreateView.as_view(), name='frase_util_create'),
    path('admin/frase-util/<int:pk>/update/', frase.FraseUtilUpdateView.as_view(), name='frase_util_update'),
    path('admin/frase-util/<int:pk>/delete/', frase.FraseUtilDeleteView.as_view(), name='frase_util_delete'),

    # ================================
    # CRUD INFORMACIÓN TOUR
    # ================================
    path('admin/informacion-tour/', tour.InformacionTourListView.as_view(), name='informacion_tour_list'),
    path('admin/informacion-tour/create/', tour.InformacionTourCreateView.as_view(), name='informacion_tour_create'),
    path('admin/informacion-tour/<int:pk>/update/', tour.InformacionTourUpdateView.as_view(), name='informacion_tour_update'),
    path('admin/informacion-tour/<int:pk>/delete/', tour.InformacionTourDeleteView.as_view(), name='informacion_tour_delete'),

    # ================================
    # CRUD TIP CULTURAL
    # ================================
    path('admin/tip-cultural/', tip_cultural.TipCulturalListView.as_view(), name='tip_cultural_list'),
    path('admin/tip-cultural/create/', tip_cultural.TipCulturalCreateView.as_view(), name='tip_cultural_create'),
    path('admin/tip-cultural/<int:pk>/update/', tip_cultural.TipCulturalUpdateView.as_view(), name='tip_cultural_update'),
    path('admin/tip-cultural/<int:pk>/delete/', tip_cultural.TipCulturalDeleteView.as_view(), name='tip_cultural_delete'),

    # ================================
    # CRUD FAVORITOS
    # ================================
    path('admin/favoritos/', favoritos.FavoritosListView.as_view(), name='favoritos_list'),
    path('admin/favoritos/create/', favoritos.FavoritosCreateView.as_view(), name='favoritos_create'),
    path('admin/favoritos/<int:pk>/update/', favoritos.FavoritosUpdateView.as_view(), name='favoritos_update'),
    path('admin/favoritos/<int:pk>/delete/', favoritos.FavoritosDeleteView.as_view(), name='favoritos_delete'),

    path('favoritos/clear/', favoritos.FavoritosClearView.as_view(), name='favoritos_clear'),
    path('favoritos/add/<int:tip_id>/', favoritos.AddFavoriteView.as_view(), name='add_favorite'),
    path('favoritos/toggle/<int:pais_id>/', favoritos.ToggleFavoritePaisView.as_view(), name='toggle_favorite_pais'),
    path('mis-favoritos/', favoritos.MisFavoritosView.as_view(), name='mis_favoritos'),

    # ================================
    # CRUD HISTORIAL
    # ================================
    path('admin/historial/', historial.HistorialListView.as_view(), name='historial_list'),
    path('admin/historial/create/', historial.HistorialCreateView.as_view(), name='historial_create'),
    path('admin/historial/<int:pk>/update/', historial.HistorialUpdateView.as_view(), name='historial_update'),
    path('admin/historial/<int:pk>/delete/', historial.HistorialDeleteView.as_view(), name='historial_delete'),
    path('historial/clear/', historial.HistorialClearView.as_view(), name='historial_clear'),
]

