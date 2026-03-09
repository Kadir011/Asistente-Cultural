from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.utils.translation import activate
from django.contrib import messages
from core.security.forms.user import UserRegisterForm
from django.contrib.auth import login, logout
from django.utils.translation import gettext_lazy as _
from django.db.models import Count
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from core.assistant.models import Favoritos, Historial, TipCultural
from django.contrib.auth import get_user_model

User = get_user_model()

# View para ingresar al sistema
class UserLoginView(LoginView):
    model = User
    template_name = 'security/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('assistant:home')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, f'Bienvenido {user.username}')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Usuario o contraseña incorrectos')
        return super().form_invalid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['username'].label = 'Nombre de usuario'
        form.fields['password'].label = 'Contraseña'
        return form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Inicio de Sesión'
        context['boton'] = self.success_url
        return context
    
# View para registrar un nuevo usuario 
class UserRegisterView(CreateView):
    template_name = 'security/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('security:login')

    def dispatch(self, request, *args, **kwargs):
        activate('es')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro de Usuario'
        context['boton'] = self.success_url
        return context

# View para cerrar sesión
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('security:login')

    def dispatch(self, request, *args, **kwargs):
        """Permite tanto GET como POST para logout"""
        if request.method == 'GET':
            return self.get(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Maneja peticiones GET para logout"""
        if request.user.is_authenticated:
            username = request.user.username
            logout(request)
            messages.success(request, f'Hasta luego {username}, has cerrado sesión exitosamente.')
        return redirect(self.next_page)

    def post(self, request, *args, **kwargs):
        """Maneja peticiones POST para logout"""
        if request.user.is_authenticated:
            username = request.user.username
            messages.success(request, f'Hasta luego {username}, has cerrado sesión exitosamente.')
        return super().post(request, *args, **kwargs) 
    
# View para la página del perfil del usuario
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'security/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        context['user'] = user
        context['title'] = 'Mi Perfil'
        
        favoritos_count = Favoritos.objects.filter(usuario=user).count()
        historial_count = Historial.objects.filter(usuario=user).count()
        
        paises_favoritos = Favoritos.objects.filter(
            usuario=user
        ).values('tip__pais').distinct().count()
        
        paises_visitados = Historial.objects.filter(
            usuario=user
        ).values('pais').distinct().count()
        
        context['stats'] = {
            'favoritos_count': favoritos_count,
            'historial_count': historial_count,
            'paises_favoritos': paises_favoritos,
            'paises_visitados': paises_visitados,
        }
        
        context['favoritos_recientes'] = Favoritos.objects.filter(
            usuario=user
        ).select_related('tip', 'tip__pais').order_by('-fecha_guardado')[:5]
        
        context['historial_reciente'] = Historial.objects.filter(
            usuario=user
        ).select_related('pais').order_by('-fecha_consulta')[:5]
        
        # Filtrar registros con pais__id no nulo
        paises_populares = Historial.objects.filter(
            usuario=user,
            pais__id__isnull=False  # Excluir registros con pais nulo
        ).values('pais__nombre', 'pais__id').annotate(
            visitas=Count('pais')
        ).order_by('-visitas')[:3]
        
        # Depuración
        print("Paises populares:", list(paises_populares))
        context['paises_populares'] = paises_populares
        return context 
    



