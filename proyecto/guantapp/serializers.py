from rest_framework import serializers
from rest_framework import exceptions
from django.contrib.auth import authenticate, login
from guantapp.models import User, UserProfile, Marca
#from guantapp.models import User, UserProfile, Marca, Producto

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
        UserProfile.objects.create(user=user, **profile_data)
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

class MarcaSerializer(serializers.ModelSerializer):
    
    user_profile=serializers.ReadOnlyField(source='user_profile.id')
    #user_profile=serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Marca
        fields = ['nombre', 'slogan', 'descripcion','user_profile']


"""class ProductoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Producto
        fields=['marca','nombre','precio','descripcion']"""

