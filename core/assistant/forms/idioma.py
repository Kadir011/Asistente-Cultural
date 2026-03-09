from django.forms import ModelForm
from django import forms 
from core.assistant.models import IdiomaOficial

# Formulario para crear un nuevo idioma oficial
class IdiomaOficialForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicar clases CSS a todos los campos
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200'
            })
    
    class Meta:
        model = IdiomaOficial
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ej: Español, Inglés, Francés'
            })
        } 







