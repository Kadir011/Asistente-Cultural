from django.forms import ModelForm
from django import forms
from core.assistant.models import TipCultural

# Formulario para crear un nuevo tipo de cultural
class TipCulturalForm(ModelForm):
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
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({
                    'class': 'w-4 h-4 text-orange-500 focus:ring-orange-400 border-gray-300 rounded'
                })
            else:
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200'
                })
    
    class Meta:
        model = TipCultural
        fields = '__all__'
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Título del tip cultural'}),
            'contenido': forms.Textarea(attrs={'placeholder': 'Contenido del tip cultural'}),
            'orden': forms.NumberInput(attrs={'min': 0, 'placeholder': 'Orden de aparición'})
        } 




