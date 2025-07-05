from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.db.models import Q
from core.assistant.forms.tip_cultural import TipCulturalForm
from core.assistant.models import TipCultural
from core.assistant.mixins.superuser import SuperUserRequiredMixin

# Views para CRUD de los tips culturales
class TipCulturalListView(SuperUserRequiredMixin, ListView):
    model = TipCultural
    template_name = 'assistant/tip_cultural/tip_cultural_list.html'
    context_object_name = 'tips_culturales'
    paginate_by = 20

    def get_queryset(self):
        q = self.request.GET.get('q')
        query = Q()
        if q is not None:
            query.add(Q(pais__nombre__icontains=q)|
                       Q(categoria__nombre__icontains=q)|
                       Q(tipo_viajero__nombre__icontains=q)|
                       Q(titulo__icontains=q)|
                       Q(contenido__icontains=q), Q.OR) 
        return self.model.objects.filter(query).order_by('pais__nombre', 'categoria__nombre', 'orden') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tips Culturales'
        context['create_url'] = reverse_lazy('assistant:tip_cultural_create')
        return context

class TipCulturalCreateView(SuperUserRequiredMixin, CreateView):
    model = TipCultural
    form_class = TipCulturalForm
    template_name = 'assistant/tip_cultural/tip_cultural_form.html'
    success_url = reverse_lazy('assistant:tip_cultural_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrar Tip Cultural'
        context['grabar'] = 'Crear Tip Cultural'
        context['back_url'] = self.success_url
        return context 

class TipCulturalUpdateView(SuperUserRequiredMixin, UpdateView):
    model = TipCultural
    form_class = TipCulturalForm
    template_name = 'assistant/tip_cultural/tip_cultural_form.html'
    success_url = reverse_lazy('assistant:tip_cultural_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Tip Cultural'
        context['grabar'] = 'Editar Tip Cultural'
        context['back_url'] = self.success_url
        return context 

class TipCulturalDeleteView(SuperUserRequiredMixin, DeleteView):
    model = TipCultural
    template_name = 'assistant/tip_cultural/tip_cultural_delete.html'
    success_url = reverse_lazy('assistant:tip_cultural_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Tip Cultural'
        context['grabar'] = 'Eliminar Tip Cultural'
        context['description'] = f'¿Está seguro de eliminar el tip cultural: {self.object.titulo or self.object.contenido[:50]}?'
        context['back_url'] = self.success_url
        return context

