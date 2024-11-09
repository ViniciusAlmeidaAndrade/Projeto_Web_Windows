from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#Essa aqui é a tabela no banco de dados responsavel por armazernar os dados do estoque
class Produtos(models.Model):
    id_prod = models.AutoField(primary_key= True)
    nome_prod = models.CharField(max_length = 150, null =  False, unique = True)
    vlr_prod = models.DecimalField(max_digits = 6, decimal_places = 2, default = 0)
    qntd_prod = models.IntegerField(default = 0)
    entrada_prod = models.DateField()
    saida_prod = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.nome_prod