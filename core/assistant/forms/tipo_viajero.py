from django.forms import ModelForm 
from django import forms
from core.assistant.models import TipoViajero

# Formulario para crear un nuevo tipo de viajero
class TipoViajeroForm(ModelForm):
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
        model = TipoViajero
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej: Aventurero, Familiar, Lujo'}),
            'descripcion': forms.Textarea(attrs={'placeholder': 'Descripción del tipo de viajero'}),
            'icono': forms.TextInput(attrs={'placeholder': 'Ej: fas fa-hiking, fas fa-family'}),
        } 


