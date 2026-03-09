from django.urls import path
from core.security.views import user

app_name = 'security'

urlpatterns = [
    path('login/', user.UserLoginView.as_view(), name='login'),
    path('registro/', user.UserRegisterView.as_view(), name='register'),
    path('logout/', user.UserLogoutView.as_view(), name='logout'), 
    path('perfil/', user.ProfileView.as_view(), name='profile'),
]

