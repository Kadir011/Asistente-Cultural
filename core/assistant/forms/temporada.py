from django.forms import ModelForm
from django import forms
from core.assistant.models import Temporada

# Formulario para crear una nueva temporada
class TemporadaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200 appearance-none bg-white'
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200',
                    'rows': 3
                })
            else:
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200'
                })
    
    class Meta:
        model = Temporada
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej: Temporada Cálida y Húmeda'}),
            'mes_inicio': forms.NumberInput(attrs={'min': 1, 'max': 12, 'placeholder': '1-12'}),
            'mes_fin': forms.NumberInput(attrs={'min': 1, 'max': 12, 'placeholder': '1-12'}),
            'descripcion': forms.Textarea(attrs={'placeholder': 'Descripción de la temporada'})
        } 







