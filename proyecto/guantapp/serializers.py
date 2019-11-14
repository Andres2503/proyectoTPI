from rest_framework import serializers
from guantapp.models import User, UserProfile, Marca

class UserProfileSerializer(serializers.ModelSerializer):                
    class Meta:
        model = UserProfile
        fields = ('profile_picture', 'phone','country', 'city', 'nit','nrc')

class UserSerializer(serializers.HyperlinkedModelSerializer):        
    profile = UserProfileSerializer(required=True)
    
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
    #
        instance.first_name=validated_data.get('first_name',instance.first_name)
        instance.last_name=validated_data.get('last_name',instance.last_name)
        instance.username=validated_data.get('username',instance.username)        

    #
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
    
    #user_profile=serializers.ReadOnlyField(source='user.id')
    user_profile=serializers.ReadOnlyField(source='user_profile.id')

    class Meta:
        model = Marca
        fields = ['nombre', 'slogan', 'descripcion','user_profile']