from django.contrib import admin
from .models import Produtos

# Register your models here.

#Aqui é a parte é a parte responsavel por deixar os dados do banco de dados mais apresentaveis no painel de administrador
@admin.register(Produtos)
class ProdutosAdmin(admin.ModelAdmin):
    list_display = ('id_prod', 'nome_prod', 'vlr_prod', 'qntd_prod', 'entrada_prod') #Isso é para aparece a tabela no /admin, caso queira alterar por lá.