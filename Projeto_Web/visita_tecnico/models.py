from django.db import models
from django.contrib.auth.models import User

class RelatoriosVisitas(models.Model):
    id_visita = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=150, null=False)
    nom_tecnico = models.CharField(max_length=150, null=False)
    nom_tecnico_f = models.CharField(max_length=150)
    nom_cliente = models.CharField(max_length=150, null=False)
    endereco = models.CharField(max_length=250, null=False)
    data = models.DateField(null=False, blank=True)
    prod_usado = models.CharField(max_length=255, null=False)
    observacao = models.TextField(null=False, blank=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return f'Tecnico: {self.nom_tecnico}, Cliente:  {self.nom_cliente}'