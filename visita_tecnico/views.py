from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import RelatoriosVisitas
from sistema.models import Produtos
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator
from django.contrib.auth import logout
import csv
import datetime

def logout_view(request):
    logout(request)
    return redirect('tela_login')

@login_required
def relatorio_vist(request):
    if request.method == "GET":
        return render(request, 'relatorio_vist.html')
    else:
        nom_tecnicos = request.POST.get("nom_tecnicos")
        
        if nom_tecnicos == request.user.username:
            relatorio = RelatoriosVisitas(
                nom_tecnico = request.POST.get("nom_tecnicos_real"),
                nom_tecnico_f = request.POST.get("nom_tecnicos_real_f"),
                usuario = nom_tecnicos,
                nom_cliente = request.POST.get("nom_clientes"),
                endereco = request.POST.get("enderecos"),
                data = request.POST.get("datas"),
                prod_usado = request.POST.get("prod_usados"),
                observacao = request.POST.get("observacoes"),
                user = request.user
            )
            relatorio.save()
            verrelat = RelatoriosVisitas.objects.all()
            return render(request, 'historico.html', {'add': True, 'verrelat': verrelat})
        else:
            return render(request, 'relatorio_vist.html', {'erro': True})
   
@login_required
def historico(request): #Aqui é a views responsavel pela parte do historico em si
    #Isso assegura que o estoque seja atualizado toda vez que entrar na pagina, isso pela por conta da variavel 'verprod'
    if request.method == 'GET':
        verrelat = RelatoriosVisitas.objects.all()
        return render(request, 'historico.html', {'verrelat': verrelat})
    
@has_role_decorator('gerente')
def deletar_visita(request, id_visita):
    #Estou puxando o objeto do banco de dados, se esse objeto por algum motivo não existir, vai retornar um erro 404. Eu estou puxando o produto pelo id, pois o id sempre será unico
    visita = get_object_or_404(RelatoriosVisitas, id_visita = id_visita)

    if request.method == 'POST':
        #Em resumo, estou deletando o produto, após isso, ele redireciona ao estoque
        visita.delete()
        return redirect('historico')
    
    #Rendirizei a página junto ao produto que eu selecionei
    return render(request, 'deletar_visita.html', {'visita': visita})


@has_role_decorator('gerente')
def exportar_csv(request):#Aqui eu estou usando a biblioteca do python csv junto a funções do django(para ser sincero, entendi nada, mas usei a documentação que esta no site do django)
    
    #Aqui eu defini a variavel response, e utilzei o metodo do django 'HTTPRESPONSE' para carregar o arquivo 'text/csv', entao basicamente toda vez que eu puxar a veriavel, ele vai carregar o arquivo csv
    response = HttpResponse(content_type = 'text/csv')
    #Aqui eu estou definindo o nome do arquivo baixado, filename = Produtos + data do momento que eu requisitei o download, após isso, o .csv pois o arquivo é csv
    response['Content-Disposition'] = 'attachment; filename=Relatorio_Visitas_' + str(datetime.datetime.now()) + '.csv'
    
    #Essa função csv.writer(response) é uma função do csv, integrada ao django, essa função espera que retorne um objeto, e o httpresponse retorna isso
    writer = csv.writer(response)
    #Aqui é o titulo das colunas no arquivo csv
    writer.writerow(['ID', 'Usuário', 'Técnico', 'Cliente', 'Data da Visita', 'Produtos Usado', 'Observação'])
    
    visitas = RelatoriosVisitas.objects.all()  #Variavel que lista todos os produtos
    
    for visita in visitas:
        writer.writerow([
            visita.id_visita,
            visita.usuario,
            visita.nom_tecnico,
            visita.nom_cliente,
            visita.data,
            visita.prod_usado,
            visita.observacao
        ])
    return response #retorna o httpresponse

@has_role_decorator('gerente') #Basicamente um copia e cola do codigo anterior
def exportar_csv_geral(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachment; filename=Relatorio_CSV_Geral_' + str(datetime.datetime.now()) + '.csv'
    
    writer = csv.writer(response)
    writer.writerow(['ID Produto', 'Nome Produto', 'Valor Produto', 'Quantidade', 'Valor Total', 'Entrada', 'Saída'])

    
    produtos = Produtos.objects.all()
    relatorios = RelatoriosVisitas.objects.all()

    total_valor = 0  
    total_produtos = 0  

    for produto in produtos:
        valor_total = produto.vlr_prod * produto.qntd_prod
        writer.writerow([
            produto.id_prod,
            produto.nome_prod,
            produto.vlr_prod,
            produto.qntd_prod,
            valor_total,
            produto.entrada_prod,
            produto.saida_prod,
        ])
        total_valor += valor_total
        total_produtos += produto.qntd_prod
        
    writer.writerow(['', 'Total Valor + Qntd:', total_valor, total_produtos, '', '', '', '', '', '', '', '', '', ''])
    writer.writerow(['', '', '', '', '', '', '']) #Espaço vazio apenas para dividir os dados
    writer.writerow(['ID Visita', 'Usuário', 'Técnico', 'Cliente', 'Data da Visita', 'Produtos Usado', 'Observação'])
    
    for relatorio in relatorios:
        writer.writerow([
            relatorio.id_visita,
            relatorio.usuario,
            relatorio.nom_tecnico,
            relatorio.nom_cliente,
            relatorio.data,
            relatorio.prod_usado,
            relatorio.observacao
        ])

    return response