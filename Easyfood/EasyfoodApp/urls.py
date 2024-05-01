from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from EasyfoodApp.views import home, products, login, product_detail, recommendations

urlpatterns = [
    #path('principal/', home, name='home' ),
    path('', home, name='home' ),
    path('productos/', products, name='products' ),
    path('login/', login, name='login'),
    path('detalles/<str:product_name>/', product_detail, name='product_detail'),
    path('recomendaciones/', recommendations, name='recommendations')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)