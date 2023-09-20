from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum, F, Q
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
    productos = articulo.objects.annotate(nlote=F('lote__lote'), fecha_ven=F('lote__fecha_vencimiento'), compra=F('lote__precio_compra')).order_by('fecha_ven')
    # queryset = request.GET.get('buscar')
    # if queryset:
    #     productos = Post.objects.filter(
    #         Q(nombre__icontains = queryset),
    #         Q(lote__icontains = queryset)
    #     )

    return render(request, 'inventario.html',{'productos': productos})
def ventas(request):
    return render(request, 'agregarProducto.html',{})
def catalogo(request):
    return render(request, 'catalogo.html',{})
