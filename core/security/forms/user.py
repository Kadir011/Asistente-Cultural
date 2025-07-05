from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from core.security.models import User
from core.assistant.models import TipoViajero
from django import forms

# Formulario para crear un nuevo usuario
class UserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        # Labels
        self.fields['first_name'].label = 'Nombre'
        self.fields['last_name'].label = 'Apellido'
        self.fields['email'].label = 'Correo electrónico'
        self.fields['username'].label = 'Nombre de usuario'
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar contraseña'
        self.fields['address'].label = 'Dirección'
        self.fields['gender'].label = 'Género'
        self.fields['tipo_viajero'].label = 'Tipo de viajero'

        # Clases CSS para todos los campos
        base_input_classes = 'w-full pl-10 pr-10 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200'
        select_classes = 'w-full pl-10 pr-10 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200 appearance-none bg-white'

        # Aplicar clases a campos de texto
        for field_name in ['first_name', 'last_name', 'email', 'username', 'address']:
            self.fields[field_name].widget.attrs.update({
                'class': base_input_classes,
                'placeholder': f'Ingresa tu {self.fields[field_name].label.lower()}'
            })
        
        # Campos de contraseña
        for field_name in ['password1', 'password2']:
            self.fields[field_name].widget.attrs.update({
                'class': base_input_classes,
                'placeholder': f'Ingresa tu {self.fields[field_name].label.lower()}'
            })
        
        # Campos select (dropdown)
        for field_name in ['gender', 'tipo_viajero']:
            self.fields[field_name].widget.attrs.update({
                'class': select_classes
            }) 
        
        # Hacer campos requeridos
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['address'].required = True

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'address', 'gender', 'tipo_viajero']
        widgets = {
            'gender': forms.Select(choices=[
                ('', 'Selecciona tu género'),
                ('M', 'Masculino'),
                ('F', 'Femenino'),
            ]),
        }
        help_texts = {
            'username': _('Solo se aceptan letras o estos caracteres @/./+/-/_ '),
            'password2': _('Vuelve a ingresar la misma contraseña'),
            'password1': _('Tu contraseña no debe ser similar a tu usuario.\n'
                           'Debe contener al menos 8 caracteres\n'
                           'No uses contraseñas habituales\n'
                           'No debe ser solo números'),
            'email': _('Ingresa un correo electrónico válido'),
            'first_name': _('Ingresa tu nombre'),
            'last_name': _('Ingresa tu apellido'),
            'address': _('Ingresa tu dirección'),
            'gender': _('Selecciona tu género (opcional)'),
            'tipo_viajero': _('Selecciona tu tipo de viajero (opcional)'),
        } 

# Formulario para ingresar al sistema
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        
        # Labels
        self.fields['username'].label = 'Nombre de usuario'
        self.fields['password'].label = 'Contraseña'
        
        # Clases CSS
        base_input_classes = 'w-full pl-10 pr-10 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200'
        
        # Aplicar clases
        self.fields['username'].widget.attrs.update({
            'class': base_input_classes,
            'placeholder': 'Ingresa tu nombre de usuario'
        })
        
        self.fields['password'].widget.attrs.update({
            'class': base_input_classes,
            'placeholder': 'Ingresa tu contraseña'
        })

# Formulario para editar el perfil del usuario
class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicar clases CSS a todos los campos
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200 appearance-none bg-white'
                })
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200',
                    'type': 'date'
                })
            else:
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200'
                })

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone_number', 
            'address', 'date_of_birth', 'gender', 'tipo_viajero'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Tu nombre'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Tu apellido'}),
            'email': forms.EmailInput(attrs={'placeholder': 'tu@email.com'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '0987654321'}),
            'address': forms.TextInput(attrs={'placeholder': 'Tu dirección completa'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(choices=[
                ('', 'Selecciona tu género'),
                ('M', 'Masculino'),
                ('F', 'Femenino')
            ]),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Este correo electrónico ya está en uso.')
        return email

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        if phone and User.objects.filter(phone_number=phone).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Este número de teléfono ya está en uso.')
        return phone 







