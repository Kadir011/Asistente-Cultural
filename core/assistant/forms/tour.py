from django.forms import ModelForm
from django import forms
from core.assistant.models import InformacionTour

# Formulario para crear una nueva información de tour 
class InformacionTourForm(ModelForm):
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
                    'rows': 4
                })
            else:
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200'
                })
    
    class Meta:
        model = InformacionTour
        fields = '__all__'
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Ej: Tener En Cuenta'}),
            'descripcion': forms.Textarea(attrs={'placeholder': 'Descripción del tour'}),
            'duracion': forms.TextInput(attrs={'placeholder': 'Ej: 4 horas desde ubicación actual'}),
            'idiomas': forms.TextInput(attrs={'placeholder': 'Ej: Inglés - Español'}),
            'precio_desde': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Precio desde'}),
            'incluye': forms.Textarea(attrs={'placeholder': 'Qué incluye el tour', 'rows': 3}),
            'icono': forms.TextInput(attrs={'placeholder': 'Ej: fas fa-clock, fas fa-language'})
        } 



    
