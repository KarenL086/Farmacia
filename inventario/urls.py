from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views
from .views import *

urlpatterns = [
    path('', views.inicioAdmin, name='inicio Administrador'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/',include('django.contrib.auth.urls'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('accounts/password_change/',include('django.contrib.auth.urls'), name='password_change'),
    # path('accounts/password_change/done/',include('django.contrib.auth.urls'), name='password_change_done'),
    # path('accounts/password_reset/',include('django.contrib.auth.urls'), name='password_reset'),
    # path('accounts/password_reset/done/',include('django.contrib.auth.urls'), name='password_reset_done'),
    # path('accounts/reset/<uidb64>/<token>/',include('django.contrib.auth.urls'), name='password_reset_confirm'),
    # path('accounts/reset/done/', include('django.contrib.auth.urls'),name='password_reset_complete'),
    path('admin/', admin.site.urls),
    path('inicioAdmin/', views.inicioAdmin, name='inicio Administrador'),
    path('login/',views.login, name="login"),
    # path('inicio/', views.inicio, name='inicio'),
    path('inventario/', views.inventario, name='inventario'),
    path('ventas/', views.ventas, name='ventas'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('crear/', views.crear, name='crear'),
    path('asignarLote/', views.asignarLote, name='asignarLote'),
    path('modificar/<id>/', views.modificar_articulo_lote, name='modificar'),
    path('eliminarProducto/<id>/', views.eliminar, name='eliminarProducto'),
    path('crearVenta/',views.crearVenta,name='crearVenta'),
    path('editarVenta/<id>/', views.editarVenta, name='editarVenta'),
    path('crearDetalleVenta/',views.crearDetalleVenta,name='crearDetalleVenta'),
    path('eliminarVenta/<int:id>/', views.eliminarVenta, name='eliminarVenta'),
    path('search',search, name="search"),
    path('search2',search2, name="search2"),
    path('searchv',searchv, name="searchv"),
    path('eliminarVenta/<id>/', views.eliminar, name='eliminarVenta'),
]

