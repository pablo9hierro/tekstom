from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

class NumeroTelefone(models.Model):
    numero = models.CharField(max_length=11, unique=True, null=True)  # Campo único para o número de telefone

    def __str__(self):
        return self.numero

    @classmethod
    def get_or_create(cls, numero):
        # Método para buscar ou criar um número de telefone único
        try:
            instance, created = cls.objects.get_or_create(numero=numero)
            return instance, created
        except cls.MultipleObjectsReturned:
            # Em caso de múltiplos objetos retornados (duplicados), exclua todos, exceto o primeiro
            duplicates = cls.objects.filter(numero=numero)
            instance_to_keep = duplicates.first()
            for duplicate in duplicates[1:]:
                duplicate.delete()
            return instance_to_keep, False

class Relatorio(models.Model):
    numero_telefone = models.ForeignKey(NumeroTelefone, on_delete=models.CASCADE)
    texto_livre = models.TextField()  # Área de texto para texto livre
    velocidade_resposta = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])  # Velocidade de resposta de 0 a 10
    nivel_engajamento = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])  # Nível de engajamento de 0 a 10
    comprometido = models.BooleanField()  # Campo para indicar se está comprometido ou não
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp para registrar a data e horário de geração do relatório
    apelido = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Apelido'))

    def __str__(self):
        return f"Relatório gerado em {self.timestamp}"

