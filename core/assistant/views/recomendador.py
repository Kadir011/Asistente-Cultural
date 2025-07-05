from django.views.generic import TemplateView
from django.db.models import Q
from core.assistant.models import Pais, TipCultural, Favoritos, Historial, TipoViajero
from django.contrib.auth.mixins import LoginRequiredMixin

# View para la página de recomendaciones
class RecommendationView(LoginRequiredMixin, TemplateView):
    template_name = 'assistant/recomendador.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Recomendaciones Culturales'
        context['paises'] = Pais.objects.all()
        context['tipos_viajero'] = TipoViajero.objects.all()

        # Obtener parámetros de búsqueda
        pais_id = self.request.GET.get('pais')
        tipo_viajero_id = self.request.GET.get('tipo_viajero')
        query = Q()

        if pais_id:
            query &= Q(pais__id=pais_id)
        if tipo_viajero_id:
            query &= Q(tipo_viajero__id=tipo_viajero_id)

        # Filtrar tips culturales
        tips = TipCultural.objects.filter(query).order_by('?')[:5]
        context['tips_culturales'] = tips

        # Agregar favoritos del usuario
        favoritos_ids = Favoritos.objects.filter(usuario=self.request.user).values_list('tip__id', flat=True)
        context['favoritos_ids'] = list(favoritos_ids)

        # Registrar en Historial si hay filtros aplicados
        if pais_id or tipo_viajero_id:
            Historial.objects.create(
                usuario=self.request.user,
                pais=Pais.objects.get(id=pais_id) if pais_id else None,
                tipo_viajero=TipoViajero.objects.get(id=tipo_viajero_id) if tipo_viajero_id else None
            )
        return context 
    
