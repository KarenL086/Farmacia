from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('inicioAdmin/', views.inicioAdmin, name='inicio Administrador'),
    path('inicio/', views.inicio, name='inicio'),
    path('inventario/', views.inventario, name='inventario'),
    path('ventas/', views.ventas, name='ventas'),
    path('catalogo/', views.catalogo, name='catalogo'),
]
