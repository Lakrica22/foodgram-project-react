from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls, name='admin.url'),
    path('api/', include('api.urls'), name='api.urls'),
    path('api/', include('users.urls'), name='users.urls'),
]