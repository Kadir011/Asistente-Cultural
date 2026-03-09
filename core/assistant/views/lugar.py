from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _  
from django.urls import reverse_lazy
from django.db.models import Q
from core.assistant.forms.lugar import LugarForm
from core.assistant.models import Lugar
from core.assistant.mixins.superuser import SuperUserRequiredMixin

# Views para CRUD de los lugares
class LugarListView(SuperUserRequiredMixin, ListView):
    model = Lugar
    template_name = 'assistant/lugar/lugar_list.html'
    context_object_name = 'lugares'
    paginate_by = 20

    def get_queryset(self):
        q = self.request.GET.get('q')
        query = Q()
        if q:
            query.add(Q(nombre__icontains=q)|Q(pais__nombre__icontains=q)|Q(region__icontains=q), Q.OR)
        return self.model.objects.filter(query).order_by('pais__nombre', 'region', 'nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lugares'
        context['create_url'] = reverse_lazy('assistant:lugar_create')
        return context

class LugarCreateView(SuperUserRequiredMixin, CreateView):
    model = Lugar
    form_class = LugarForm
    template_name = 'assistant/lugar/lugar_form.html'
    success_url = reverse_lazy('assistant:lugar_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Lugar'
        context['grabar'] = 'Crear Lugar'
        context['back_url'] = self.success_url
        return context

class LugarUpdateView(SuperUserRequiredMixin, UpdateView):
    model = Lugar
    form_class = LugarForm
    template_name = 'assistant/lugar/lugar_form.html'
    success_url = reverse_lazy('assistant:lugar_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Lugar'
        context['grabar'] = 'Actualizar Lugar'
        context['back_url'] = self.success_url
        return context

class LugarDeleteView(SuperUserRequiredMixin, DeleteView):
    model = Lugar
    template_name = 'assistant/lugar/lugar_delete.html'
    success_url = reverse_lazy('assistant:lugar_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Lugar'
        context['grabar'] = 'Eliminar Lugar'
        context['description'] = f'¿Está seguro de eliminar el lugar: {self.object.nombre}?'
        context['back_url'] = self.success_url
        return context