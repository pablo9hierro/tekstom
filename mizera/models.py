from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

class NumeroTelefone(models.Model):
    numero = models.CharField(max_length=11)  # Campo para armazenar o número de telefone

    def __str__(self):
        return self.numero
    

class Relatorio(models.Model):
    texto_livre = models.TextField()  # Área de texto para texto livre
    velocidade_resposta = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])  # Velocidade de resposta de 0 a 10
    nivel_engajamento = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])  # Nível de engajamento de 0 a 10
    comprometido = models.BooleanField()  # Campo para indicar se está comprometido ou não
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp para registrar a data e horário de geração do relatório
    apelido = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Apelido'))

    def __str__(self):
        return f"Relatório gerado em {self.timestamp}"