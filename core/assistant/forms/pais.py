from django.forms import ModelForm 
from django import forms
from core.assistant.models import Pais

# Formulario para crear un nuevo pais
class PaisForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicar clases CSS
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200 appearance-none bg-white'
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200',
                    'rows': 4
                })
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200'
                })
            else:
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200'
                })
    
    class Meta:
        model = Pais
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre del país'}),
            'codigo_iso': forms.TextInput(attrs={'placeholder': 'Ej: ECU, PER, COL'}),
            'descripcion_corta': forms.Textarea(attrs={'placeholder': 'Descripción breve del país', 'rows': 3}),
            'descripcion_completa': forms.Textarea(attrs={'placeholder': 'Descripción detallada del país', 'rows': 6}),
            'ubicacion': forms.TextInput(attrs={'placeholder': 'Ej: Ecuador - Islas Galápagos'}),
            'capital': forms.TextInput(attrs={'placeholder': 'Capital del país'}),
            'moneda': forms.TextInput(attrs={'placeholder': 'Ej: Dólar americano, Sol peruano'}),
            'latitud': forms.NumberInput(attrs={'placeholder': 'Ej: -0.1807', 'step': '0.00000001'}),
            'longitud': forms.NumberInput(attrs={'placeholder': 'Ej: -78.4678', 'step': '0.00000001'}),
            'poblacion': forms.NumberInput(attrs={'placeholder': 'Población aproximada'}),
            'superficie': forms.NumberInput(attrs={'placeholder': 'Superficie en km²', 'step': '0.01'}),
        } 





