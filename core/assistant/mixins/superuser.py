from django.contrib.auth.mixins import UserPassesTestMixin

# Mixin para permitir acceso a las vistas solo para superusuarios
class SuperUserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser 
    


