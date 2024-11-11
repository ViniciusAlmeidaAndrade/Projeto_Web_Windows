from rolepermissions.roles import AbstractUserRole
from django.contrib.auth.models import User

class Gerente(AbstractUserRole):
    available_permissions = {'editar_estoque': True}

class Tecnico(AbstractUserRole):
    available_permissions = {'ver_estoque': True}