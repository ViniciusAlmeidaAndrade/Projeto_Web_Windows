from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.tela_login, name = 'tela_login'),
    path('sistema/', include('sistema.urls'))
]