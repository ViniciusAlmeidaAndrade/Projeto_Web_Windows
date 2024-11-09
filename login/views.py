from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from sistema import urls

def tela_login(request): #Views responsavel por autenticar o usuario
    #Renderizo o html pelo metodo get
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        #Puxo o username e password do form, e verifico se é valido, se for, eu prossigo para a tela inicial, se não for, aparece um pop-up
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)

        if user is None:
            return render(request, 'login.html', {'usuario_invalido': True})
        else:
            login(request, user)
            return redirect('sistema/estoque')