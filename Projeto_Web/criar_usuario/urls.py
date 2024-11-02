from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.criar_usuario, name = 'criar_usuario'), #URL responsavel por ser a tela inicial do redirect, ela enviar para o formulario de criar usuario
    path('lista', views.lista_usuarios, name = 'lista'), #URL responsavel por encaminhar para a lista de funcionarios
    path('mudar_senha/<int:id>', views.mudar_senha, name = 'editar'),  #URL responsavel por encaminhar para o html de mudar senha
    path('deletar/<int:id>', views.deletar_usuario, name = 'deletar'), #URL responsavel por encaminhar para o html de deletar usuario
    path('mudar_informações/<int:id>', views.modificar_usuario, name = 'mudar_informações'), #URL responsavel por encaminhar para o html de moodificar usuario
    path('logout/', views.logout_view, name = 'logout'), #URL responsavel por fazer o logout do usuario
]