from django.forms import ModelForm
from django import forms
from core.assistant.models import Favoritos

# Formulario para crear un nuevo favorito
class FavoritosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200 appearance-none bg-white'
                })
    
    class Meta:
        model = Favoritos
        fields = '__all__'


