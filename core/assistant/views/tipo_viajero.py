from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.db.models import Q 
from core.assistant.forms.tipo_viajero import TipoViajeroForm   
from core.assistant.models import TipoViajero
from core.assistant.mixins.superuser import SuperUserRequiredMixin 

# Views para CRUD de los tipos de viajero
class TipoViajeroListView(SuperUserRequiredMixin, ListView):
    model = TipoViajero
    template_name = 'assistant/tipo_viajero/tipo_viajero_list.html'
    context_object_name = 'tipos_viajero'
    paginate_by = 20

    def get_queryset(self):
        q = self.request.GET.get('q')
        query = Q()
        if q:
            query.add(Q(nombre__icontains=q)|Q(descripcion__icontains=q), Q.OR)
        return self.model.objects.filter(query).order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tipos de Viajero'
        context['create_url'] = reverse_lazy('assistant:tipo_viajero_create')
        return context

class TipoViajeroCreateView(SuperUserRequiredMixin, CreateView):
    model = TipoViajero
    form_class = TipoViajeroForm
    template_name = 'assistant/tipo_viajero/tipo_viajero_form.html'
    success_url = reverse_lazy('assistant:tipo_viajero_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Tipo de Viajero'
        context['grabar'] = 'Crear Tipo'
        context['back_url'] = self.success_url
        return context

class TipoViajeroUpdateView(SuperUserRequiredMixin, UpdateView):
    model = TipoViajero
    form_class = TipoViajeroForm
    template_name = 'assistant/tipo_viajero/tipo_viajero_form.html'
    success_url = reverse_lazy('assistant:tipo_viajero_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Tipo de Viajero'
        context['grabar'] = 'Actualizar Tipo'
        context['back_url'] = self.success_url
        return context

class TipoViajeroDeleteView(SuperUserRequiredMixin, DeleteView):
    model = TipoViajero
    template_name = 'assistant/tipo_viajero/tipo_viajero_delete.html'
    success_url = reverse_lazy('assistant:tipo_viajero_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Tipo de Viajero'
        context['grabar'] = 'Eliminar Tipo'
        context['description'] = f'¿Está seguro de eliminar el tipo de viajero: {self.object.nombre}?'
        context['back_url'] = self.success_url
        return context