from django.forms import ModelForm
from django import forms
from core.assistant.models import FraseUtil

# Formulario para crear una nueva frase útil
class FraseUtilForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200 appearance-none bg-white'
                })
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200',
                    'accept': 'audio/*'
                })
            else:
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200'
                })
    
    class Meta:
        model = FraseUtil
        fields = '__all__'
        widgets = {
            'frase_espanol': forms.TextInput(attrs={'placeholder': 'Ej: Hola, ¿cómo estás?'}),
            'frase_local': forms.TextInput(attrs={'placeholder': 'Ej: Hello, how are you?'}),
            'pronunciacion': forms.TextInput(attrs={'placeholder': 'Ej: jelow, jau ar yu'}),
            'categoria': forms.TextInput(attrs={'placeholder': 'Ej: saludo, comida, transporte'})
        }

