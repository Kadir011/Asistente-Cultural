from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.db.models import Q
from core.assistant.forms.favoritos import FavoritosForm
from core.assistant.models import Favoritos, TipCultural, Pais, Categoria, TipoViajero 
from core.assistant.mixins.superuser import SuperUserRequiredMixin 
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Views para CRUD de los favoritos
class FavoritosListView(SuperUserRequiredMixin, ListView):
    model = Favoritos
    template_name = 'assistant/favoritos/favoritos_list.html'
    context_object_name = 'favoritos'
    paginate_by = 20

    def get_queryset(self):
        q = self.request.GET.get('q') 
        query = Q() 
        if q is not None:
            query.add(Q(usuario__username__icontains=q) |
                       Q(tip__pais__nombre__icontains=q)|
                       Q(tip__titulo__icontains=q), Q.OR)
            return Favoritos.objects.filter(query).order_by('-fecha_guardado')
        return Favoritos.objects.all().order_by('-fecha_guardado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Favoritos'
        context['create_url'] = reverse_lazy('assistant:favoritos_create')
        return context

class FavoritosCreateView(SuperUserRequiredMixin, CreateView):
    model = Favoritos 
    template_name = 'assistant/favoritos/favoritos_form.html'
    form_class = FavoritosForm
    success_url = reverse_lazy('assistant:favoritos_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrar Favoritos'
        context['grabar'] = 'Crear Favorito'
        context['back_url'] = self.success_url
        return context

class FavoritosUpdateView(SuperUserRequiredMixin, UpdateView):
    model = Favoritos
    template_name = 'assistant/favoritos/favoritos_form.html'
    form_class = FavoritosForm
    success_url = reverse_lazy('assistant:favoritos_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Favoritos'
        context['grabar'] = 'Editar Favorito'
        context['back_url'] = self.success_url
        return context

class FavoritosDeleteView(SuperUserRequiredMixin, DeleteView):
    model = Favoritos
    template_name = 'assistant/favoritos/favoritos_delete.html'
    success_url = reverse_lazy('assistant:favoritos_list') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Favoritos'
        context['grabar'] = 'Eliminar Favoritos'
        context['description'] = f'¿Está seguro de eliminar el favorito: {self.object.usuario.username} - {self.object.tip.pais.nombre}?'
        context['back_url'] = self.success_url
        return context 
    

# Views para añadir/eliminar favoritos
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, tip_id, *args, **kwargs):
        try:
            tip = TipCultural.objects.get(id=tip_id)
            favorite = Favoritos.objects.filter(usuario=self.request.user, tip=tip)
            if favorite.exists():
                favorite.delete()
                return JsonResponse({
                    'success': True,
                    'is_favorite': False,
                    'message': 'El tip cultural ha sido eliminado de favoritos.'
                })
            else:
                Favoritos.objects.create(usuario=self.request.user, tip=tip)
                return JsonResponse({
                    'success': True,
                    'is_favorite': True,
                    'message': 'El tip cultural ha sido añadido a favoritos.'
                })
        except TipCultural.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'El tip cultural no existe.'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al procesar la solicitud: {str(e)}'
            }, status=500)

# View para vaciar todos los favoritos
class FavoritosClearView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, 'No tienes permiso para realizar esta acción.')
            return redirect('assistant:favoritos_list')

        Favoritos.objects.all().delete()
        messages.success(request, 'Todos los favoritos han sido vaciados exitosamente.')
        return redirect('assistant:favoritos_list') 
    
# View para añadir/eliminar favoritos
@method_decorator(csrf_exempt, name='dispatch')
class ToggleFavoritePaisView(LoginRequiredMixin, View):    
    def get(self, request, pais_id):
        """Verificar si un país está en favoritos"""
        try:
            pais = Pais.objects.get(id=pais_id)
            is_favorite = Favoritos.objects.filter(
                usuario=request.user,
                tip__pais=pais
            ).exists()
            
            return JsonResponse({
                'success': True,
                'is_favorite': is_favorite,
                'pais_nombre': pais.nombre
            })
            
        except Pais.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'País no encontrado'
            }, status=404)
    
    def post(self, request, pais_id):
        """Toggle favorito para un país"""
        try:
            pais = Pais.objects.get(id=pais_id)
            
            # Buscar si ya existe algún favorito para este país (cualquier tip del país)
            favorito_existente = Favoritos.objects.filter(
                usuario=request.user, 
                tip__pais=pais
            ).first()
            
            if favorito_existente:
                # Si existe, lo eliminamos
                favorito_existente.delete()
                is_favorite = False
                message = f'{pais.nombre} ha sido eliminado de tus favoritos'
            else:
                # Si no existe, buscamos cualquier tip del país para crear el favorito
                tip_del_pais = TipCultural.objects.filter(pais=pais).first()
                
                if tip_del_pais:
                    Favoritos.objects.create(
                        usuario=request.user,
                        tip=tip_del_pais
                    )
                    is_favorite = True
                    message = f'{pais.nombre} ha sido añadido a tus favoritos'
                else:
                    # Si no hay tips para este país, crear uno genérico
                    categoria_default = Categoria.objects.first()
                    tipo_viajero_default = TipoViajero.objects.first()
                    
                    if not categoria_default:
                        return JsonResponse({
                            'success': False,
                            'message': 'No hay categorías disponibles. Contacta al administrador.'
                        }, status=500)
                    
                    if not tipo_viajero_default:
                        return JsonResponse({
                            'success': False,
                            'message': 'No hay tipos de viajero disponibles. Contacta al administrador.'
                        }, status=500)
                    
                    tip_generico = TipCultural.objects.create(
                        pais=pais,
                        categoria=categoria_default,
                        tipo_viajero=tipo_viajero_default,
                        contenido=f"País favorito: {pais.nombre}",
                        titulo=f"Favorito - {pais.nombre}"
                    )
                    
                    Favoritos.objects.create(
                        usuario=request.user,
                        tip=tip_generico
                    )
                    is_favorite = True
                    message = f'{pais.nombre} ha sido añadido a tus favoritos'
            
            return JsonResponse({
                'success': True,
                'is_favorite': is_favorite,
                'message': message
            })
            
        except Pais.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'País no encontrado'
            }, status=404)
        except Exception as e:
            # Log del error para debug
            import logging
            logging.error(f"Error en ToggleFavoritePaisView: {str(e)}")
            
            return JsonResponse({
                'success': False,
                'message': f'Error al procesar la solicitud'
            }, status=500)

# View para mostrar los favoritos del usuario
class MisFavoritosView(LoginRequiredMixin, ListView):  
    model = Favoritos
    template_name = 'assistant/mis_favoritos.html'
    context_object_name = 'favoritos'
    paginate_by = 12

    def get_queryset(self):
        return Favoritos.objects.filter(
            usuario=self.request.user
        ).select_related('tip', 'tip__pais', 'tip__categoria').order_by('-fecha_guardado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mis Favoritos'
        
        # Agrupar favoritos por país para evitar duplicados
        favoritos_agrupados = {}
        for favorito in context['favoritos']:
            if favorito.tip and favorito.tip.pais:
                pais_id = favorito.tip.pais.id
                if pais_id not in favoritos_agrupados:
                    favoritos_agrupados[pais_id] = {
                        'favorito': favorito,
                        'pais': favorito.tip.pais,
                        'tips_count': 0
                    }
                favoritos_agrupados[pais_id]['tips_count'] += 1
        
        context['favoritos_agrupados'] = list(favoritos_agrupados.values())
        return context

