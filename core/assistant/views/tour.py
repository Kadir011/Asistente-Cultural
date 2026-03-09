from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.db.models import Q
from core.assistant.forms.tour import InformacionTourForm
from core.assistant.models import InformacionTour
from core.assistant.mixins.superuser import SuperUserRequiredMixin

# Views para CRUD de los tours
class InformacionTourUpdateView(SuperUserRequiredMixin, UpdateView):
    model = InformacionTour
    form_class = InformacionTourForm
    template_name = 'assistant/informacion_tour/informacion_tour_form.html'
    success_url = reverse_lazy('assistant:informacion_tour_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Info de Tour'
        context['grabar'] = 'Actualizar Info'
        context['back_url'] = self.success_url
        return context

class InformacionTourDeleteView(SuperUserRequiredMixin, DeleteView):
    model = InformacionTour
    template_name = 'assistant/informacion_tour/informacion_tour_delete.html'
    success_url = reverse_lazy('assistant:informacion_tour_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Info de Tour'
        context['grabar'] = 'Eliminar Info'
        context['description'] = f'¿Está seguro de eliminar la información: {self.object.titulo}?'
        context['back_url'] = self.success_url
        return context

class InformacionTourListView(SuperUserRequiredMixin, ListView):
    model = InformacionTour
    template_name = 'assistant/informacion_tour/informacion_tour_list.html'
    context_object_name = 'tours'
    paginate_by = 20

    def get_queryset(self):
        q = self.request.GET.get('q')
        query = Q()
        if q:
            query.add(Q(titulo__icontains=q)|Q(pais__nombre__icontains=q)|Q(descripcion__icontains=q), Q.OR)
        return self.model.objects.filter(query).order_by('pais__nombre', 'titulo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Información de Tours'
        context['create_url'] = reverse_lazy('assistant:informacion_tour_create')
        return context

class InformacionTourCreateView(SuperUserRequiredMixin, CreateView):
    model = InformacionTour
    form_class = InformacionTourForm
    template_name = 'assistant/informacion_tour/informacion_tour_form.html'
    success_url = reverse_lazy('assistant:informacion_tour_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Info de Tour'
        context['grabar'] = 'Crear Info'
        context['back_url'] = self.success_url
        return context

class InformacionTourUpdateView(SuperUserRequiredMixin, UpdateView):
    model = InformacionTour
    form_class = InformacionTourForm
    template_name = 'assistant/informacion_tour/informacion_tour_form.html'
    success_url = reverse_lazy('assistant:informacion_tour_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Info de Tour'
        context['grabar'] = 'Actualizar Info'
        context['back_url'] = self.success_url
        return context

class InformacionTourDeleteView(SuperUserRequiredMixin, DeleteView):
    model = InformacionTour
    template_name = 'assistant/informacion_tour/informacion_tour_delete.html'
    success_url = reverse_lazy('assistant:informacion_tour_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Info de Tour'
        context['grabar'] = 'Eliminar Info'
        context['description'] = f'¿Está seguro de eliminar la información: {self.object.titulo}?'
        context['back_url'] = self.success_url
        return context 
    
