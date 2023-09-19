from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum, F
from .models import articulo, lote

# Create your views here.
def inicioAdmin(request):
    datos = articulo.objects.annotate(total_cantidad=Sum('lote__cantidad_stock'), fecha_ven=F('lote__fecha_vencimiento')).order_by('idarticulo') 
    return render(request, 'inicioAdmin.html',{'datos': datos})
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
