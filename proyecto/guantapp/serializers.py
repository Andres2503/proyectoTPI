from rest_framework import serializers
from rest_framework import exceptions
from django.contrib.auth import authenticate, login
from guantapp.models import User, UserProfile, Marca, Producto, ListaDeseos, Categoria, Calificacion, Orden, Pago, LineaOrden


##### Serializers relacionados a usuario
class UserProfileSerializer(serializers.ModelSerializer):                
    class Meta:
        model = UserProfile
        fields = ('profile_picture', 'phone','country', 'city', 'nit','nrc')

class UserSerializer(serializers.HyperlinkedModelSerializer):        
    profile = UserProfileSerializer(required=True)
    
    password = serializers.CharField(
        max_length=128,
        #min_length=8,
        min_length=4,
        write_only=True
    )
    
    class Meta:
        model = User        
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)        
        user.set_password(password)        
        user.save()        
        profile=UserProfile.objects.create(user=user, **profile_data)                
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.profile_picture = profile_data.get('profile_picture', profile.profile_picture)        
        profile.phone = profile_data.get('phone', profile.phone)
        profile.country = profile_data.get('country', profile.country)
        profile.city = profile_data.get('city', profile.city)
        profile.nit = profile_data.get('nit', profile.nit)
        profile.nrc = profile_data.get('nrc', profile.nrc)
        profile.save()

        return instance

##### Serializers relacionados a marca
class MarcaSerializer(serializers.ModelSerializer):    
    user_profile=serializers.ReadOnlyField(source='user_profile.id')    

    class Meta:
        model = Marca
        fields = ['nombre', 'slogan', 'descripcion','user_profile']

##### Serializers relacionados a categoria
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Categoria
        fields=['nombre','descripcion','parent']
    
class CategoriaReadSerializer(CategoriaSerializer):
    parent=CategoriaSerializer(read_only=True)


"""class CategoriaReadSerializer(CategoriaSerializer):                    

    def get_parent(self,obj):
        value=super().to_representation(obj)
        if value.parent is None:
            parent = CategoriaReadSerializer(read_only=True)
        else:            
            parent = CategoriaSerializer(read_only=True)"""
        
        

##### Serializers relacionados a producto
class ProductoSerializer(serializers.ModelSerializer):        
    #marca=MarcaSerializer(many=True)
    class Meta:
        model=Producto
        fields=['marca','nombre','precio','descripcion','categoria']

class ProductoReadSerializer(ProductoSerializer):
    marca=MarcaSerializer(read_only=True)
    #categoria=CategoriaSerializer(read_only=True)
    categoria=CategoriaReadSerializer(read_only=True)

class ProductoCategoriaReadSerializer(serializers.ModelSerializer):
    marca=MarcaSerializer(read_only=True)    

####### Serializers relacionados a ListaDeseo
class ListaDeseosSerializer(serializers.ModelSerializer):         
    user_profile=serializers.ReadOnlyField(source='user_profile.id')        

    class Meta:
        model=ListaDeseos
        fields=['user_profile','producto']
    
class ListaDeseosReadSerializer(ListaDeseosSerializer):
    #user_profile=UserProfileSerializer(read_only=True)
    producto=ProductoSerializer(read_only=True)

##### Serializers relacionados a Calificacion
class CalificacionSerializer(serializers.ModelSerializer):
    user_profile=serializers.ReadOnlyField(source='user_profile.id')    
    class Meta:
        model=Calificacion
        fields=['valor_calificacion','producto','descripcion','user_profile']

class CalificacionReadSerializer(CalificacionSerializer):
    producto=ProductoSerializer(read_only=True)

##### Serializers relacionados a Pago
class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Pago
        fields=['__all__']


##### Serializers relacionados a LineaOrden
class LineaOrdenSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=LineaOrden
        fields=['__all__']


##### Serializers relacionados a Orden
class OrdenSerializer(serializers.ModelSerializer):    
    comprador=serializers.ReadOnlyField(source='user_profile.id')
    class Meta:
        model=Orden
        fields=['comprador','pago','vendedor']

##### Serializers relacionados a LineaOrden

class LineaOrdenSerializer(serializers.ModelSerializer):
    class Meta:
        model=LineaOrden
        fields=['__all__']
    
class LineaOrdenReadSerializer(LineaOrdenSerializer):
    producto=ProductoSerializer(read_only=True)
    orden=OrdenSerializer(read_only=True)
