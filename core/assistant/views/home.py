from django.views.generic import TemplateView, FormView
from core.assistant.models import Pais, TipCultural, GaleriaImagen
from core.assistant.forms.contacto import ContactForm
from core.assistant.mixins.superuser import SuperUserRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

User = get_user_model()

# View para la página principal
class HomeView(TemplateView):
    template_name = 'components/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'TravelWorld - Viaja Inteligente'
        
        # Datos para mostrar en el home
        context['total_paises'] = Pais.objects.count()
        context['paises_destacados'] = Pais.objects.all()[:6]
        context['tips_recientes'] = TipCultural.objects.all()[:3]
        return context 

# View para la página de Sobre Nosotros
class AboutView(TemplateView):
    template_name = 'components/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'About'
        return context
    
# View para la página de Contacto
class ContactView(FormView):
    template_name = 'components/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('assistant:contact')

    def form_valid(self, form):
        nombre = form.cleaned_data['nombre']
        email = form.cleaned_data['email']
        asunto = form.cleaned_data['asunto']
        mensaje = form.cleaned_data['mensaje']

        # Enviar correo
        send_mail(
            subject=f'{asunto} - {nombre}',
            message=f'Nombre: {nombre}\nCorreo: {email}\nMensaje: {mensaje}',
            from_email=email,
            recipient_list=['kbarquetb@unemi.edu.ec'],
            fail_silently=False,
        )
        messages.success(self.request, 'Tu mensaje ha sido enviado exitosamente.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contáctanos'
        return context 
    
# View para la página de Menú
class MenuView(SuperUserRequiredMixin, TemplateView):
    template_name = 'components/menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Panel de Administración'
        # Estadísticas para el dashboard
        context['total_paises'] = Pais.objects.count()
        context['total_tips'] = TipCultural.objects.count()
        context['total_usuarios'] = User.objects.count()
        context['total_imagenes'] = GaleriaImagen.objects.count()
        return context 



