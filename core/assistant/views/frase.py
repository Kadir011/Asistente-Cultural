from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.db.models import Q
from core.assistant.forms.frase import FraseUtilForm
from core.assistant.models import FraseUtil
from core.assistant.mixins.superuser import SuperUserRequiredMixin

# Views para CRUD de las frases útiles
class FraseUtilListView(SuperUserRequiredMixin, ListView):
    model = FraseUtil
    template_name = 'assistant/frase_util/frase_util_list.html'
    context_object_name = 'frases'
    paginate_by = 20

    def get_queryset(self):
        q = self.request.GET.get('q')
        query = Q()
        if q:
            query.add(Q(frase_espanol__icontains=q)|Q(frase_local__icontains=q)|Q(pais__nombre__icontains=q), Q.OR)
        return self.model.objects.filter(query).order_by('pais__nombre', 'categoria')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Frases Útiles'
        context['create_url'] = reverse_lazy('assistant:frase_util_create')
        return context

class FraseUtilCreateView(SuperUserRequiredMixin, CreateView):
    model = FraseUtil
    form_class = FraseUtilForm
    template_name = 'assistant/frase_util/frase_util_form.html'
    success_url = reverse_lazy('assistant:frase_util_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Frase Útil'
        context['grabar'] = 'Crear Frase'
        context['back_url'] = self.success_url
        return context

class FraseUtilUpdateView(SuperUserRequiredMixin, UpdateView):
    model = FraseUtil
    form_class = FraseUtilForm
    template_name = 'assistant/frase_util/frase_util_form.html'
    success_url = reverse_lazy('assistant:frase_util_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Frase Útil'
        context['grabar'] = 'Actualizar Frase'
        context['back_url'] = self.success_url
        return context

class FraseUtilDeleteView(SuperUserRequiredMixin, DeleteView):
    model = FraseUtil
    template_name = 'assistant/frase_util/frase_util_delete.html'
    success_url = reverse_lazy('assistant:frase_util_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Frase Útil'
        context['grabar'] = 'Eliminar Frase'
        context['description'] = f'¿Está seguro de eliminar la frase: {self.object.frase_espanol}?'
        context['back_url'] = self.success_url
        return context