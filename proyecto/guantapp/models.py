from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class User(AbstractUser):
    username = models.CharField(null=False, unique=True,max_length=50)
    email = models.EmailField(_('email address'), unique=True, null=False)
    first_name=models.CharField(null=False, max_length=50)
    last_name=models.CharField(null=False, max_length=50)    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']    

    def __str__(self):
        return "{}".format(self.email) 

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    profile_picture=models.CharField(max_length=100)
    phone=models.CharField(max_length=8)        
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    nit = models.CharField(max_length=14)
    nrc = models.CharField(max_length=50)       

class Marca(models.Model):
    user_profile=models.ForeignKey(UserProfile,null=False, on_delete=models.CASCADE, related_name='marca')
    nombre=models.CharField(max_length=50, null=False)
    slogan=models.CharField(max_length=50, null=False)
    descripcion=models.CharField(max_length=50, null=False)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return "{}".format(self.nombre)


"""class Producto(models.Model):
    marca=models.ForeignKey(Marca, null=False, on_delete=models.CASCADE, related_name='marca')
    nombre=models.CharField(max_length=50, null=False)
    precio=models.CharField(max_length=50, null=False)
    descripcion=models.TextField(null=False, default='descripción del producto')"""