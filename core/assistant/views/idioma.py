from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.db.models import Q
from core.assistant.forms.idioma import IdiomaOficialForm
from core.assistant.models import IdiomaOficial
from core.assistant.mixins.superuser import SuperUserRequiredMixin

# Views para CRUD de los idiomas oficiales
class IdiomaOficialListView(SuperUserRequiredMixin, ListView):
    model = IdiomaOficial
    template_name = 'assistant/idioma_oficial/idioma_oficial_list.html'
    context_object_name = 'idiomas'
    paginate_by = 20

    def get_queryset(self):
        q = self.request.GET.get('q')
        query = Q()
        if q:
            query.add(Q(nombre__icontains=q), Q.OR)
        return self.model.objects.filter(query).order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Idiomas Oficiales'
        context['create_url'] = reverse_lazy('assistant:idioma_oficial_create')
        return context

class IdiomaOficialCreateView(SuperUserRequiredMixin, CreateView):
    model = IdiomaOficial
    form_class = IdiomaOficialForm
    template_name = 'assistant/idioma_oficial/idioma_oficial_form.html'
    success_url = reverse_lazy('assistant:idioma_oficial_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Idioma Oficial'
        context['grabar'] = 'Crear Idioma'
        context['back_url'] = self.success_url
        return context

class IdiomaOficialUpdateView(SuperUserRequiredMixin, UpdateView):
    model = IdiomaOficial
    form_class = IdiomaOficialForm
    template_name = 'assistant/idioma_oficial/idioma_oficial_form.html'
    success_url = reverse_lazy('assistant:idioma_oficial_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Idioma Oficial'
        context['grabar'] = 'Actualizar Idioma'
        context['back_url'] = self.success_url
        return context

class IdiomaOficialDeleteView(SuperUserRequiredMixin, DeleteView):
    model = IdiomaOficial
    template_name = 'assistant/idioma_oficial/idioma_oficial_delete.html'
    success_url = reverse_lazy('assistant:idioma_oficial_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Idioma Oficial'
        context['grabar'] = 'Eliminar Idioma'
        context['description'] = f'¿Está seguro de eliminar el idioma: {self.object.nombre}?'
        context['back_url'] = self.success_url
        return context 
    


