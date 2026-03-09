from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.db.models import Q
from core.assistant.forms.temporada import TemporadaForm
from core.assistant.models import Temporada
from core.assistant.mixins.superuser import SuperUserRequiredMixin

# Views para CRUD de las temporadas
class TemporadaListView(SuperUserRequiredMixin, ListView):
    model = Temporada
    template_name = 'assistant/temporada/temporada_list.html'
    context_object_name = 'temporadas'
    paginate_by = 20

    def get_queryset(self):
        q = self.request.GET.get('q')
        query = Q()
        if q:
            query.add(Q(nombre__icontains=q)|Q(pais__nombre__icontains=q)|Q(tipo__icontains=q), Q.OR)
        return self.model.objects.filter(query).order_by('pais__nombre', 'mes_inicio')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Temporadas'
        context['create_url'] = reverse_lazy('assistant:temporada_create')
        return context

class TemporadaCreateView(SuperUserRequiredMixin, CreateView):
    model = Temporada
    form_class = TemporadaForm
    template_name = 'assistant/temporada/temporada_form.html'
    success_url = reverse_lazy('assistant:temporada_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Temporada'
        context['grabar'] = 'Crear Temporada'
        context['back_url'] = self.success_url
        return context

class TemporadaUpdateView(SuperUserRequiredMixin, UpdateView):
    model = Temporada
    form_class = TemporadaForm
    template_name = 'assistant/temporada/temporada_form.html'
    success_url = reverse_lazy('assistant:temporada_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Temporada'
        context['grabar'] = 'Actualizar Temporada'
        context['back_url'] = self.success_url
        return context

class TemporadaDeleteView(SuperUserRequiredMixin, DeleteView):
    model = Temporada
    template_name = 'assistant/temporada/temporada_delete.html'
    success_url = reverse_lazy('assistant:temporada_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Temporada'
        context['grabar'] = 'Eliminar Temporada'
        context['description'] = f'¿Está seguro de eliminar la temporada: {self.object.nombre}?'
        context['back_url'] = self.success_url
        return context