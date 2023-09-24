from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum, F, Q
from datetime import datetime
from .models import lote, articulo, venta, detalle_venta
from .forms import ArticuloForm

# Create your views here.
def inicioAdmin(request):
    datos = articulo.objects.annotate(total_cantidad=Sum('lote__cantidad_stock'), fecha_ven=F('lote__fecha_vencimiento')).order_by('idarticulo') 
    return render(request, 'inicioAdmin.html',{'datos': datos})

def inicio(request):
    today = datetime.today()
    ventai = articulo.objects.annotate(cant=F('detalle_venta__cantidad'), total=F('detalle_venta__cantidad')*F('precio_venta'))
    return render(request, 'inicio.html',{'ventai':ventai})

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

def crear(request):
    data = {
        'form': ArticuloForm()
    }
    if request.method == 'POST':
        formulario = ArticuloForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
        else: 
            data['form'] = formulario

    return render(request, 'medicina/crear.html', data)