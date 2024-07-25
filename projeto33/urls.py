
from django.urls import path, include
from mizera.views import upload_json, dash_def, buscar_numero_telefone, relatorio_numero, salvar_relatorio, relatorio, pagina_extrato, todosforms
from django.contrib import admin
urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', upload_json, name='formulariojson'),
    path('dash/', dash_def, name='dash'),
    path('buscar_numero_telefone/', buscar_numero_telefone, name='buscar_numero_telefone'),
    path('relatorio/<str:numero>/', relatorio_numero, name='relatorio_numero'),
    path('salvar_relatorio/', salvar_relatorio, name='salvar_relatorio'),
    path('extrato/', pagina_extrato, name='extrato'),
    path('todosforms/', todosforms, name='todosforms'),
    
    
]
   
