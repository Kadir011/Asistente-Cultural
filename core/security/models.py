from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    tipo_viajero = models.ForeignKey('assistant.TipoViajero', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Tipo de viajero')
    first_name = models.CharField(max_length=30, blank=False, null=False, verbose_name='Nombre')
    last_name = models.CharField(max_length=30, blank=False, null=False, verbose_name='Apellido')
    email = models.EmailField(unique=True, blank=False, null=False, verbose_name='Correo electrónico'   )
    phone_number = models.CharField(max_length=10, unique=True, blank=True, null=True, verbose_name='Número de teléfono')
    address = models.CharField(max_length=255, blank=False, null=False, )
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Fecha de nacimiento')
    gender = models.CharField(max_length=10, choices=[('M', 'Masculino'), ('F', 'Femenino')], blank=True, null=True, )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    groups = models.ManyToManyField(Group, related_name='security_user_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='security_user_set', blank=True)

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_username(self):
        return self.username 
    
    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.username})' 
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')







