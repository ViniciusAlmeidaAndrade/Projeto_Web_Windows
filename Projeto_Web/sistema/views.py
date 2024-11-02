from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Produtos
from visita_tecnico.models import RelatoriosVisitas
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator
from django.contrib.auth import logout
import csv
import datetime

def logout_view(request):
    logout(request)
    return redirect('tela_login')

@login_required
def estoque(request): #Aqui é a views responsavel pela parte do estoque em si
    #Isso assegura que o estoque seja atualizado toda vez que entrar na pagina, isso pela por conta da variavel 'verprod'
    if request.method == 'GET':
        verprod = Produtos.objects.all()
        return render(request, 'estoque/estoque.html', {'verprod': verprod})
    
@has_role_decorator('gerente')
def adicionar_produto(request): #Aqui é a view responsavel pela funcionalidade de adicionar produto ao estoque.
    #Primeiro eu renderizo a página pelo metódo GET
    if request.method == 'GET':
        return render(request, 'estoque/editar/adicionar.html')
    else:
        #Primeiro eu codei a verificação, isso para ver se existe um produto com o mesmo nome. 'Filter' = faz uma busca detalhada no banco de dados. 'first()' = busca o objeto.
        nome_prod = request.POST.get('nome')
        verificar = Produtos.objects.filter(nome_prod = nome_prod).first()

        #Aqui eu estou verificando se a variavel 'verificar' é verdadeira, se for, ela irá retornar um pop-up configurado no HTML, e após isso recarregar a página.
        if verificar:
            return render(request, 'estoque/editar/adicionar.html', {'nao_add': True})
        else:
            #Em resumo, eu estou salvando o produto no banco de dados, após salvar, ele irá redirecionar para a tela de estoque.
            produtos = Produtos(
            nome_prod=request.POST.get('nome'),
            vlr_prod=request.POST.get('valor'),
            qntd_prod=request.POST.get('qntd'),
            entrada_prod=request.POST.get('data_entrada'),
            user = request.user
            )
            produtos.save()

            return redirect('estoque')
        
@has_role_decorator('gerente')
def deletar_produto(request, id_prod): #Aqui é a view responsavel pela funcionalidade de remover o produto do estoque.
    #Estou puxando o objeto do banco de dados, se esse objeto por algum motivo não existir, vai retornar um erro 404. Eu estou puxando o produto pelo id, pois o id sempre será unico
    produto = get_object_or_404(Produtos, id_prod=id_prod)

    if request.method == 'POST':
        #Em resumo, estou deletando o produto, após isso, ele redireciona ao estoque
        produto.delete()
        return redirect('estoque')
    
    #Rendirizei a página junto ao produto que eu selecionei
    return render(request, 'estoque/editar/remover.html', {'produto': produto})

@has_role_decorator('gerente')
def modificar_produto(request, id_prod): #Aqui é a view responsavel pela funcionalidade de remover o produto do estoque.
    #Estou puxando o objeto do banco de dados, se esse objeto por algum motivo não existir, vai retornar um erro 404. Eu estou puxando o produto pelo id, pois o id sempre será unico
    produto = get_object_or_404(Produtos, id_prod = id_prod)
    
    if request.method == 'POST':
            #Em resumo, eu estou salvando a modificação do produto no banco de dados, após salvar, ele irá retornar um pop-up confirmando a alteração, e por fim, vai redirecionar para a tela de estoque.
            produto.nome_prod = request.POST.get('nome')
            produto.vlr_prod = request.POST.get('valor')
            produto.qtnd_prod = request.POST.get('quantidade')
            produto.entrada_prod = request.POST.get('data_entrada')

            verprod = Produtos.objects.all()
            produto.save()

            return render(request, 'estoque/estoque.html', {'add': True, 'verprod': verprod})
    
    #Rendirizei a página junto ao produto que eu selecionei
    return render(request, 'estoque/editar/modificar.html', {'produto': produto})

@has_role_decorator('gerente')
def exportar_csv(request):#Aqui eu estou usando a biblioteca do python csv junto a funções do django(para ser sincero, entendi nada, mas usei a documentação que esta no site do django)
    
    #Aqui eu defini a variavel response, e utilzei o metodo do django 'HTTPRESPONSE' para carregar o arquivo 'text/csv', entao basicamente toda vez que eu puxar a veriavel, ele vai carregar o arquivo csv
    response = HttpResponse(content_type = 'text/csv')
    #Aqui eu estou definindo o nome do arquivo baixado, filename = Produtos + data do momento que eu requisitei o download, após isso, o .csv pois o arquivo é csv
    response['Content-Disposition'] = 'attachment; filename=Relatorio_Estoque_' + str(datetime.datetime.now()) + '.csv'
    
    #Essa função csv.writer(response) é uma função do csv, integrada ao djago, essa função espera que retorne um objeto, e o httpresponse retorna isso
    writer = csv.writer(response)
    #Aqui é o titulo das colunas no arquivo csv
    writer.writerow(['ID', 'Nome', 'Valor Unitário', 'Quantidade', 'Valor Total', 'Entrada', 'Saída'])
    
    produtos = Produtos.objects.all()  #Variavel que lista todos os produtos
    total_valor = 0  #Variável para armazenar a soma dos produtos
    total_produtos = 0  #Variável para armazenar o total d
    
    for produto in produtos: #Loop for para passar em todos os produtos
        valor_total = produto.vlr_prod * produto.qntd_prod  #Calcula o valor total de produtos em estoquede multiplicando a quantidade de cada produto com o valor dele 
        writer.writerow([
            produto.id_prod,
            produto.nome_prod,
            produto.vlr_prod,
            produto.qntd_prod,
            valor_total,
            produto.entrada_prod,
            produto.saida_prod
        ])
        #Aqui eu to informando que o loop vai preencher cada titulo da tabela com as informações passadas
        
        total_valor += valor_total  #Atualizada a variavel de valor total e soma a ela
        total_produtos += produto.qntd_prod  #Adiciona a quantidade de produtos a soma dos produtos
    
    #Adicionei uma linha para a o valor total dos produtos e o total de produtos
    writer.writerow(['', 'Valor total dos produtos + qntd:', total_valor, total_produtos])

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