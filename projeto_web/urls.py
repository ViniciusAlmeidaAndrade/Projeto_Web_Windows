from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404
from login import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login.urls'))
]