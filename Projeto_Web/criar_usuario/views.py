from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from rolepermissions.roles import assign_role
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('tela_login')

@has_role_decorator('gerente')
def criar_usuario(request): #Views responsavel por literalmente criar o usuario
    #Primeiro eu renderizo a página pelo metódo GET
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    else:
        #Primeiro eu codei a verificação, isso para ver se existe um usuario com o mesmo nome. 'Filter' = faz uma busca detalhada no banco de dados. 'first()' = busca o objeto.
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        
        user = User.objects.filter(username = username).first()
        #Aqui eu estou verificando se a variavel 'user' é verdadeira, se for, ela irá retornar um pop-up configurado no HTML, e após isso recarregar a página.
        if user:
            return render(request, 'cadastro.html', {'duplicado': True})
        elif password != password1:
            return render(request, 'cadastro.html', {'erro': True})
        else:
            #Em resumo, eu estou salvando o usuario no banco de dados e passando o cargo de tecnico para ele, após salvar, ele irá redirecionar para a tela de cadastro.                         
            user = User.objects.create_user(first_name = first_name, last_name = last_name, username = username, email = email, password = password)
            user.save()
            assign_role(user, 'tecnico')
            return render(request, 'cadastro.html', {'add': True})

@has_role_decorator('gerente')
def lista_usuarios(request):#Views responsavel por listar todos os usuarios presentes no sistema
    #Isso assegura que o estoque seja atualizado toda vez que entrar na pagina, isso pela por conta da variavel 'ver_user'
    ver_user = User.objects.all()
    return render(request, 'lista_users/lista.html', {'ver_user': ver_user})
    
@has_role_decorator('gerente')    
def mudar_senha(request, id): #Views responsavel por alterar a senha do usuario
    #Estou puxando o objeto do banco de dados, se esse objeto por algum motivo não existir, vai retornar um erro 404. Eu estou puxando o produto pelo id, pois o id sempre será unico
    user = get_object_or_404(User, id=id)
    
    if request.method == 'GET':
        return render(request, 'lista_users/editar.html', {'user': user})        
    else:
        #Voce ira receber a nova senha, após isso, ira salver o usuario
        nova_senha = request.POST.get('senha')
        nova_senha1 = request.POST.get('senha1')
        if nova_senha1 != nova_senha:
            #Pop-Up de senhas diferntes
            return render(request, 'lista_users/editar.html', {'erro': True})
        elif nova_senha:
            user.set_password(nova_senha)
            user.save()
            ver_user = User.objects.all()
            return render(request, 'lista_users/lista.html', {'ver_user': ver_user , 'add_senha': True})
        else:
            #Pop-up de erro
            return render(request, 'lista_users/editar.html', {'user': user , 'nao_add': True})

@has_role_decorator('gerente')            
def deletar_usuario(request, id): #Views responsavel por deletar o usuario
   #Estou puxando o objeto do banco de dados, se esse objeto por algum motivo não existir, vai retornar um erro 404. Eu estou puxando o produto pelo id, pois o id sempre será unico
    usuario = get_object_or_404(User, id = id)

    if request.method == 'POST':
        #Função para deletar o usuari, o usuario foi selecionado pelo id
        usuario.delete()
        return redirect('lista')  # Redireciona para o lista

    return render(request, 'lista_users/remover.html', {'usuario': usuario})    

@has_role_decorator('gerente')            
def modificar_usuario(request, id): #Views responsavel por editar informações do usuario (exceto senha)
    #Estou puxando o objeto do banco de dados, se esse objeto por algum motivo não existir, vai retornar um erro 404. Eu estou puxando o produto pelo id, pois o id sempre será unico
    usuario = get_object_or_404(User, id=id)
    
    username = request.POST.get('username')
    user = User.objects.filter(username = username).first()
    if user:
        return render(request, 'lista_users/modificar_info.html', {'duplicado': True, 'usuario': usuario})
    elif request.method == 'POST':
        #Recebo os dados do formulario, após isso, salvo os novos dados dele
        usuario.first_name = request.POST.get('first_name')
        usuario.last_name = request.POST.get('last_name')
        usuario.username = request.POST.get('username')
        usuario.email = request.POST.get('email')
        usuario.save()
        
        veruser = User.objects.all()
        return render(request, 'lista_users/lista.html', {'duplicado': True, 'usuario': usuario, 'ver_user': veruser})

    return render(request, 'lista_users/modificar_info.html', {'usuario': usuario})