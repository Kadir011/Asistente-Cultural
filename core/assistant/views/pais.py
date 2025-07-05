from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.db.models import Q
from core.assistant.forms.pais import PaisForm
from core.assistant.models import Pais, Favoritos, Historial
from core.assistant.mixins.superuser import SuperUserRequiredMixin

# Views para CRUD de los países
class PaisListView(SuperUserRequiredMixin, ListView):
    model = Pais
    template_name = 'assistant/pais/pais_list.html'
    context_object_name = 'paises'
    paginate_by = 20 

    def get_queryset(self):
        q = self.request.GET.get('q') 
        query = Q() 
        if q is not None:
            query.add(Q(nombre__icontains=q)|
                       Q(codigo_iso__icontains=q)|
                       Q(idioma_oficial__nombre__icontains=q)|
                       Q(capital__icontains=q), Q.OR) 
        return self.model.objects.filter(query).order_by('nombre') 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['title'] = 'Países' 
        context['create_url'] = reverse_lazy('assistant:pais_create')
        return context 

class PaisCreateView(SuperUserRequiredMixin, CreateView):
    model = Pais
    form_class = PaisForm
    template_name = 'assistant/pais/pais_form.html' 
    success_url = reverse_lazy('assistant:pais_list') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrar País'
        context['grabar'] = 'Crear País'
        context['back_url'] = self.success_url
        return context 

class PaisUpdateView(SuperUserRequiredMixin, UpdateView):
    model = Pais
    form_class = PaisForm
    template_name = 'assistant/pais/pais_form.html' 
    success_url = reverse_lazy('assistant:pais_list') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar País'
        context['grabar'] = 'Actualizar País'
        context['back_url'] = self.success_url
        return context 

class PaisDeleteView(SuperUserRequiredMixin, DeleteView):
    model = Pais
    template_name = 'assistant/pais/pais_delete.html'
    success_url = reverse_lazy('assistant:pais_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar País'
        context['grabar'] = 'Eliminar País'
        context['description'] = f'¿Está seguro de eliminar el país: {self.object.nombre}?'
        context['back_url'] = self.success_url
        return context 

# View para explorar o mostrar detalles de un país
class PaisDetailView(TemplateView):
    template_name = 'assistant/pais_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pais_id = kwargs.get('pk')
        
        try:
            pais = Pais.objects.get(id=pais_id)
            context['pais'] = pais
            context['title'] = pais.nombre
            
            # Verificar si el país está en favoritos del usuario
            if self.request.user.is_authenticated:
                is_favorite = Favoritos.objects.filter(
                    usuario=self.request.user,
                    tip__pais=pais  # Buscar por país a través del tip
                ).exists()
                context['is_favorite'] = is_favorite
            else:
                context['is_favorite'] = False
            
            # Obtener información relacionada
            context['temporadas'] = pais.temporadas.all()
            context['galeria'] = pais.galeria.all().order_by('orden')
            context['lugares'] = pais.lugares.all()
            context['normas'] = pais.normas.all().order_by('tipo', 'orden')
            context['frases_utiles'] = pais.frases_utiles.all().order_by('categoria')
            context['info_tours'] = pais.info_tours.all()
            context['tips_culturales'] = pais.tip_culturals.all().order_by('categoria__nombre', 'orden')
            
            # Registrar visita en historial si el usuario está autenticado
            if self.request.user.is_authenticated:
                Historial.objects.create(
                    usuario=self.request.user,
                    pais=pais
                )   
        except Pais.DoesNotExist:
            context['error'] = 'País no encontrado'
        return context
    
# View para listar todos los países de manera pública
class PaisListPublicView(ListView):
    model = Pais
    template_name = 'assistant/paises_public.html'
    context_object_name = 'paises'
    paginate_by = 12
    
    def get_queryset(self):
        q = self.request.GET.get('q')
        query = Q()
        if q:
            query.add(Q(nombre__icontains=q)|Q(descripcion_corta__icontains=q), Q.OR)
        return self.model.objects.filter(query).order_by('nombre')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Explora Países'
        
        # Si el usuario está autenticado, obtener sus favoritos
        if self.request.user.is_authenticated:
            favoritos_ids = Favoritos.objects.filter(
                usuario=self.request.user
            ).values_list('tip__pais__id', flat=True).distinct()
            
            context['favoritos_ids'] = list(favoritos_ids)
        else:
            context['favoritos_ids'] = []
        return context