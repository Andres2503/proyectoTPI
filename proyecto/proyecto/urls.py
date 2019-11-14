from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include, url
urlpatterns = [
    path('admin/', admin.site.urls),
    path('guantapp/', include('guantapp.urls')),
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]