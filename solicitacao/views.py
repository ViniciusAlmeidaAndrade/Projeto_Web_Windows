from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('tela_login')

@login_required
def solicitar(request): #View responsavel pela funcionalidade de enviar email ao gerente
    #Renderizando o html pelo metodo GET
    if request.method == 'GET':
        return render(request, 'solicitação.html')
    
    email = request.POST.get('email')
    assunto = request.POST.get('assunto')
    mensagem = request.POST.get('mensagem')

    #Verificando se email, assunto e mensagem é verdadeiro
    if email and assunto and mensagem:
        #Função do django responsavel por enviar o email
        send_mail(
            assunto, 
            (f'''{mensagem}
enviado por: {email}'''), 
            settings.EMAIL_HOST_USER,
            ['gerenteabreuweb@gmail.com'],
            fail_silently=False,
        )
        return render(request, 'solicitação.html', {'feito': True})
    else:
        return render(request, 'solicitação.html', {'erro': True})