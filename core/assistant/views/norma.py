from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy    
from django.db.models import Q
from core.assistant.forms.norma import NormaForm
from core.assistant.models import Norma
from core.assistant.mixins.superuser import SuperUserRequiredMixin

# Views para CRUD de las normas
class NormaListView(SuperUserRequiredMixin, ListView):
    model = Norma
    template_name = 'assistant/norma/norma_list.html'
    context_object_name = 'normas'
    paginate_by = 20

    def get_queryset(self):
        q = self.request.GET.get('q')
        query = Q()
        if q:
            query.add(Q(titulo__icontains=q)|Q(pais__nombre__icontains=q)|Q(tipo__icontains=q), Q.OR)
        return self.model.objects.filter(query).order_by('pais__nombre', 'tipo', 'orden')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Normas'
        context['create_url'] = reverse_lazy('assistant:norma_create')
        return context

class NormaCreateView(SuperUserRequiredMixin, CreateView):
    model = Norma
    form_class = NormaForm
    template_name = 'assistant/norma/norma_form.html'
    success_url = reverse_lazy('assistant:norma_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Norma'
        context['grabar'] = 'Crear Norma'
        context['back_url'] = self.success_url
        return context

class NormaUpdateView(SuperUserRequiredMixin, UpdateView):
    model = Norma
    form_class = NormaForm
    template_name = 'assistant/norma/norma_form.html'
    success_url = reverse_lazy('assistant:norma_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Norma'
        context['grabar'] = 'Actualizar Norma'
        context['back_url'] = self.success_url
        return context

class NormaDeleteView(SuperUserRequiredMixin, DeleteView):
    model = Norma
    template_name = 'assistant/norma/norma_delete.html'
    success_url = reverse_lazy('assistant:norma_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Norma'
        context['grabar'] = 'Eliminar Norma'
        context['description'] = f'¿Está seguro de eliminar la norma: {self.object.titulo}?'
        context['back_url'] = self.success_url
        return context