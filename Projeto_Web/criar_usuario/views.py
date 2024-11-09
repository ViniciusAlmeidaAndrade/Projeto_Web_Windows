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
def deletar_usuario(request, id): #Views responsavel por deletar o usuario
   #Estou puxando o objeto do banco de dados, se esse objeto por algum motivo não existir, vai retornar um erro 404. Eu estou puxando o produto pelo id, pois o id sempre será unico
    usuario = get_object_or_404(User, id = id)

    if request.method == 'POST':
        #Função para deletar o usuari, o usuario foi selecionado pelo id
        usuario.delete()
        return redirect('lista')  # Redireciona para o lista

    return render(request, 'lista_users/remover.html', {'usuario': usuario})    

@has_role_decorator('gerente')
def modificar_usuario(request, id):
    #Puxando o objeto do banco de dados, se não existir, retorna erro 404
    usuario = get_object_or_404(User, id=id)
    
    #Verifação se existe um username igual o informado
    username = request.POST.get('username')
    user = User.objects.filter(username=username).exclude(id =usuario.id).first()
    if user: #Basicamente, se user foi verdadeiro, ele retorna o pop up de erro
        return render(request, 'lista_users/modificar_info.html', {'duplicado': True, 'usuario': usuario})
    
    elif request.method == 'POST':
        # Atualiza os dados
        usuario.first_name = request.POST.get('first_name')
        usuario.last_name = request.POST.get('last_name')
        usuario.username = request.POST.get('username')
        usuario.email = request.POST.get('email')
        
        #Puxando a senha do form
        nova_senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('senha1')
        
        if nova_senha and confirmar_senha:
            if nova_senha == confirmar_senha:
                # Atualiza a senha do usuario
                usuario.set_password(nova_senha)
            else:
                return render(request, 'lista_users/modificar_info.html', {'senha': True, 'usuario': usuario})
                

        #Salva os as informações dos usuarios
        usuario.save()
        
        #Redireciona para a lista de usuarios
        veruser = User.objects.all()
        return render(request, 'lista_users/lista.html', {'add': True, 'usuario': usuario, 'ver_user': veruser})

    return render(request, 'lista_users/modificar_info.html', {'usuario': usuario})
