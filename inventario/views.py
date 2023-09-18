from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def inicioAdmin(request):
    return render(request, 'inicioAdmin.html',{})
def inicio(request):
    return render(request, 'inicio.html',{})
def index(request):
    return render(request, 'index.html',{
        'form': AuthenticationForm
    })
def inventario(request):
    return render(request, 'inventario.html',{})
def ventas(request):
    return render(request, 'agregarProducto.html',{})
def catalogo(request):
    return render(request, 'catalogo.html',{})
