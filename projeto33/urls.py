
from django.urls import path
from mizera.views import upload_json, dash_def, buscar_numero_telefone

urlpatterns = [
    path('upload/', upload_json, name='formulariojson'),
    path('dash/', dash_def, name='dash'),
    path('buscar_numero_telefone/', buscar_numero_telefone, name='buscar_numero_telefone'),
   
]