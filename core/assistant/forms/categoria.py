from django.forms import ModelForm 
from django import forms
from core.assistant.models import Categoria 

# Formulario para crear una nueva categoría
class CategoriaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200',
                    'rows': 3
                })
            else:
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200'
                })
    
    class Meta:
        model = Categoria
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre de la categoría'}),
            'descripcion': forms.Textarea(attrs={'placeholder': 'Descripción de la categoría'}),
            'icono': forms.TextInput(attrs={'placeholder': 'Ej: fas fa-utensils, fas fa-bed'}),
            'color': forms.TextInput(attrs={'type': 'color'}),
        } 

