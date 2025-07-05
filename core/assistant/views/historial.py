from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.db.models import Q
from core.assistant.forms.historial import HistorialForm
from core.assistant.models import Historial
from core.assistant.mixins.superuser import SuperUserRequiredMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

# Views para CRUD de los historiales
class HistorialListView(SuperUserRequiredMixin, ListView):
    model = Historial
    template_name = 'assistant/historial/historial_list.html'
    context_object_name = 'historiales'
    paginate_by = 20

    def get_queryset(self):
        q = self.request.GET.get('q') 
        query = Q() 
        if q is not None:
            query.add(Q(usuario__username__icontains=q)|
                       Q(pais__nombre__icontains=q)|
                       Q(tipo_viajero__nombre__icontains=q), Q.OR)
            return Historial.objects.filter(query).order_by('-fecha_consulta')
        return Historial.objects.all().order_by('-fecha_consulta')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Historial'
        context['create_url'] = reverse_lazy('assistant:historial_create')
        return context

class HistorialCreateView(SuperUserRequiredMixin, CreateView):
    model = Historial
    template_name = 'assistant/historial/historial_form.html'
    form_class = HistorialForm
    success_url = reverse_lazy('assistant:historial_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrar Historial'
        context['grabar'] = 'Crear Historial'
        context['back_url'] = self.success_url
        return context
    
class HistorialUpdateView(SuperUserRequiredMixin, UpdateView):
    model = Historial
    template_name = 'assistant/historial/historial_form.html'
    form_class = HistorialForm
    success_url = reverse_lazy('assistant:historial_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Historial'
        context['grabar'] = 'Editar Historial'
        context['back_url'] = self.success_url
        return context

class HistorialDeleteView(SuperUserRequiredMixin, DeleteView):
    model = Historial
    template_name = 'assistant/historial/historial_delete.html'
    success_url = reverse_lazy('assistant:historial_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Historial'
        context['grabar'] = 'Eliminar Historial'
        context['description'] = f'¿Está seguro de eliminar el historial: {self.object.usuario.username} - {self.object.pais.nombre if self.object.pais else "Sin país"}?'
        context['back_url'] = self.success_url
        return context

# View para vaciar el historial
class HistorialClearView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, 'No tienes permiso para realizar esta acción.')
            return redirect('assistant:historial_list')

        Historial.objects.all().delete()
        messages.success(request, 'El historial ha sido vaciado exitosamente.')
        return redirect('assistant:historial_list')

