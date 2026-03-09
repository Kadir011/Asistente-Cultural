from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.db.models import Q
from core.assistant.forms.categoria import CategoriaForm
from core.assistant.models import Categoria
from core.assistant.mixins.superuser import SuperUserRequiredMixin 

# Views para CRUD de las categorías
class CategoriaListView(SuperUserRequiredMixin, ListView):
    model = Categoria
    template_name = 'assistant/categoria/categoria_list.html'
    context_object_name = 'categorias'
    paginate_by = 20

    def get_queryset(self):
        q = self.request.GET.get('q')
        query = Q()
        if q:
            query.add(Q(nombre__icontains=q)|Q(descripcion__icontains=q), Q.OR)
        return self.model.objects.filter(query).order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Categorías'
        context['create_url'] = reverse_lazy('assistant:categoria_create')
        return context

class CategoriaCreateView(SuperUserRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'assistant/categoria/categoria_form.html'
    success_url = reverse_lazy('assistant:categoria_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Categoría'
        context['grabar'] = 'Crear Categoría'
        context['back_url'] = self.success_url
        return context

class CategoriaUpdateView(SuperUserRequiredMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'assistant/categoria/categoria_form.html'
    success_url = reverse_lazy('assistant:categoria_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Categoría'
        context['grabar'] = 'Actualizar Categoría'
        context['back_url'] = self.success_url
        return context

class CategoriaDeleteView(SuperUserRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'assistant/categoria/categoria_delete.html'
    success_url = reverse_lazy('assistant:categoria_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Categoría'
        context['grabar'] = 'Eliminar Categoría'
        context['description'] = f'¿Está seguro de eliminar la categoría: {self.object.nombre}?'
        context['back_url'] = self.success_url
        return context