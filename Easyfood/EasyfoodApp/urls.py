from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from EasyfoodApp.views import home, products, login

urlpatterns = [
    path('principal/', home, name='home' ),
    path('productos/', products, name='products' ),
    path('inicio/', login, name='login')  
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)