from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.validators import RegexValidator
from mptt.models import MPTTModel, TreeForeignKey


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
    #profile_picture=models.CharField(max_length=100)
    profile_picture=models.ImageField()
    phone=models.CharField(max_length=8, validators=[RegexValidator(regex=r"[267][0-9]{7}",message="Teléfono inválido")]) #No tiene el unique. No es necesario el max_length   
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    nit = models.CharField(max_length=14, unique=True,validators=[RegexValidator(regex=r"[0-9]{14}",message="NIT inválido")])
    #nrc = models.CharField(max_length=7, unique=True, validators=[RegexValidator(regex=r"[0-9]-[0-9]",message="NRC inválido")])       
    nrc = models.CharField(max_length=7, unique=True)       

class Marca(models.Model):
    user_profile=models.ForeignKey(UserProfile,null=False, on_delete=models.CASCADE, related_name='user_profile_Marca')#marca
    nombre=models.CharField(max_length=50, null=False)
    slogan=models.CharField(max_length=50, null=False)
    descripcion=models.TextField(max_length=200, null=False)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return "{}".format(self.nombre)


class Categoria(MPTTModel):
    nombre=models.CharField(max_length=50, null=False)
    descripcion=models.TextField(null=False, default='descripción de la categoría')
    parent=TreeForeignKey('self',null=True,blank=True, related_name='children',db_index=True, on_delete=models.CASCADE)    

    class MPTTMeta:
        order_insertion_by = ['nombre']

class Producto(models.Model):
    marca=models.ForeignKey(Marca, null=False, on_delete=models.CASCADE, related_name='marca')
    nombre=models.CharField(max_length=50, null=False)    
    precio=models.DecimalField(max_digits=10,decimal_places=2, null=False)
    descripcion=models.TextField(null=False, default='descripción del producto')
    categoria=models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='categoria')

class ListaDeseos(models.Model):
    user_profile=models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_profile_lista_deseos')
    producto=models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='productos')

class Calificacion(models.Model):
    valor_calificacion=models.CharField(max_length=1)#suponiendo valor 1 al 5
    producto=models.ForeignKey(Producto,null=False,on_delete=models.CASCADE)
    user_profile=models.ForeignKey(UserProfile,null=False,on_delete=models.CASCADE)
    descripcion=models.TextField(null=False, default='descripción de la calificación')


class Orden(models.Model):    
    num_orden=models.AutoField(primary_key=True)
    fecha=models.DateField(auto_now=False,auto_now_add=False)
    hora=models.TimeField(auto_now=False, auto_now_add=False)
    estado=models.IntegerField()#Pendiente, duda con los valores de borrador, pagado, etc
    vendedor=models.ForeignKey(UserProfile,null=False,on_delete=models.CASCADE,related_name='vendedor')
    comprador=models.ForeignKey(UserProfile,null=False,on_delete=models.CASCADE,related_name='comprador')


class Pago(models.Model):
    monto=models.DecimalField(max_digits=10,decimal_places=2,null=False)    
    fecha=models.DateField(auto_now=False,auto_now_add=False)
    metodo_pago=models.IntegerField()#Duda
    orden=models.OneToOneField(Orden,null=False,on_delete=models.CASCADE)

    
class LineaOrden(models.Model):
    cantidad=models.IntegerField()
    #subtotal=models.DecimalField(max_digits=10,decimal_places=2,null=False)
    precio_unitario=models.DecimalField(max_digits=10,decimal_places=2,null=False)#duda con campo
    orden=models.ForeignKey(Orden,null=False,on_delete=models.CASCADE)
    producto=models.ForeignKey(Producto,null=False,on_delete=models.CASCADE)

    @property
    def subtotal(self):
        return '{subtotal}'.format(subtotal=precio_unitario*cantidad)

