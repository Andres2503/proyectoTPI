from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include, url
from rest_framework.authtoken import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('guantapp/', include('guantapp.urls')),
    path('login',jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),      
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]

#Login control normal de usuario
"""urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]"""
