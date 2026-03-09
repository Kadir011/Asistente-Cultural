from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.db.models import Q
from core.assistant.forms.galeria import GaleriaImagenForm
from core.assistant.models import GaleriaImagen
from core.assistant.mixins.superuser import SuperUserRequiredMixin

# Views para CRUD de las galerías de imágenes
class GaleriaImagenListView(SuperUserRequiredMixin, ListView):
    model = GaleriaImagen
    template_name = 'assistant/galeria_imagen/galeria_imagen_list.html'
    context_object_name = 'imagenes'
    paginate_by = 20

    def get_queryset(self):
        q = self.request.GET.get('q')
        query = Q()
        if q:
            query.add(Q(titulo__icontains=q)|Q(pais__nombre__icontains=q), Q.OR)
        return self.model.objects.filter(query).order_by('pais__nombre', 'orden')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Galería de Imágenes'
        context['create_url'] = reverse_lazy('assistant:galeria_imagen_create')
        return context

class GaleriaImagenCreateView(SuperUserRequiredMixin, CreateView):
    model = GaleriaImagen
    form_class = GaleriaImagenForm
    template_name = 'assistant/galeria_imagen/galeria_imagen_form.html'
    success_url = reverse_lazy('assistant:galeria_imagen_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Subir Imagen'
        context['grabar'] = 'Subir Imagen'
        context['back_url'] = self.success_url
        return context

class GaleriaImagenUpdateView(SuperUserRequiredMixin, UpdateView):
    model = GaleriaImagen
    form_class = GaleriaImagenForm
    template_name = 'assistant/galeria_imagen/galeria_imagen_form.html'
    success_url = reverse_lazy('assistant:galeria_imagen_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Imagen'
        context['grabar'] = 'Actualizar Imagen'
        context['back_url'] = self.success_url
        return context

class GaleriaImagenDeleteView(SuperUserRequiredMixin, DeleteView):
    model = GaleriaImagen
    template_name = 'assistant/galeria_imagen/galeria_imagen_delete.html'
    success_url = reverse_lazy('assistant:galeria_imagen_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Imagen'
        context['grabar'] = 'Eliminar Imagen'
        context['description'] = f'¿Está seguro de eliminar la imagen: {self.object.titulo or "Sin título"}?'
        context['back_url'] = self.success_url
        return context