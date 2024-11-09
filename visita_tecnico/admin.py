from django.contrib import admin
from.models import RelatoriosVisitas

admin.site.register(RelatoriosVisitas)
class ProdutosAdmin(admin.ModelAdmin):
    list_display = ('id_prod', 'nome_prod', 'vlr_prod', 'qntd_prod', 'entrada_prod') #Isso é para aparece a tabela no /admin, caso queira alterar por lá.