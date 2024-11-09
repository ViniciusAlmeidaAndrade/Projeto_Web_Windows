from django.urls import path, include
from . import views
from solicitacao import urls

urlpatterns = [
    path('estoque/', views.estoque, name = 'estoque'), #Aqui é aonde o sistema sempre irá se inicializar após fazer login, no caso, é o estoque
    path('estoque/adicionar/', views.adicionar_produto, name = 'add_estoque'), #Essa é a url responsavel por redirecionar para a página de adicionar um produto, página essa, que so o gerente terá acesso
    path('estoque/editar/<int:id_prod>/', views.modificar_produto, name='editar_produto'), #Essa é a url responsavel por redirecionar para a página de editar um produto, página essa, que so o gerente terá acesso
    path('estoque/deletar/<int:id_prod>/', views.deletar_produto, name='deletar_produto'), #Essa é a url responsavel por redirecionar para a página de deletar um produto, página essa, que so o gerente terá acesso
    
    path('criar_usuario/', include('criar_usuario.urls'), name = 'criar_usuario'), #Aqui é estou dando um redirect para as urls da parte de criar usuarios
    path('solicitação/', include('solicitacao.urls'), name = 'enviar_solicitação'), #Aqui é estou dando um redirect para as urls da parte de enviar solicitação por email
    path('visita_tecnica/', include('visita_tecnico.urls'), name = 'visita_tecnico'), #Aqui é estou dando um redirect para as urls da parte de informar visita tecnica

    path('exportar_csv/', views.exportar_csv, name = 'exportar_csv'),

     path('exportar_csv_geral/', views.exportar_csv_geral, name = 'exportar_csv_geral'),

    path('logout/', views.logout_view, name = 'logout'), #URL responsavel por fazer o logout do usuario
]