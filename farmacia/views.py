from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
# from .models import 

def inicioAdmin(request):
    return render(request, 'inicioAdmin.html',{})
def inicio(request):
    return render(request, 'inicio.html',{})
def login(request):
    return render(request, 'login.html',{
        'form': AuthenticationForm
    })
def inventario(request):
    return render(request, 'inventario.html',{})
def ventas(request):
    return render(request, 'agregarProducto.html',{})
def catalogo(request):
    return render(request, 'catalogo.html',{})
