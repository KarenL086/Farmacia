from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum, F, Q
from datetime import date
from .models import articulo, lote
from .forms import ArticuloForm

# Create your views here.

def login(request):
    return render(request, 'login.html',{
        'form': AuthenticationForm
    })

def group_required1(GrupoAdmin):
    def check_group(User):
        return User.groups.filter(name=GrupoAdmin).exists()
    return user_passes_test(check_group)

def group_required(GrupoUser):
    def check_group(User):
        return User.groups.filter(name=GrupoUser).exists()
    return user_passes_test(check_group)

#@login_required
#@group_required1('GrupoAdmin')
def inicioAdmin(request):
    # datos = articulo.objects.annotate(total_cantidad=Sum('lote__cantidad_stock'), fecha_ven=F('lote__fecha_vencimiento')).order_by('idarticulo') 
    # return render(request, 'inicioAdmin.html',{'datos': datos})
    venta= articulo.objects.filter(detalle_venta__idventa__fecha_hora=date.today()).annotate(total=Sum('detalle_venta__cantidad') * F('precio_venta'), cantidad=F('detalle_venta__cantidad')).values('nombre', 'cantidad', 'total')
    return render(request, 'inicio.html',{'venta':venta})
#@login_required
#@group_required1('GrupoAdmin')
def inventario(request):
    productos = articulo.objects.annotate(nlote=F('lote__lote'), fecha_ven=F('lote__fecha_vencimiento'), compra=F('lote__precio_compra')).order_by('fecha_ven')


    return render(request, 'inventario.html',{'productos': productos})
#@login_required
#@group_required1('GrupoAdmin')
def ventas(request):
    return render(request, 'agregarProducto.html',{})

#@login_required
#@group_required('GrupoUser')
def inicio(request):
    venta= articulo.objects.filter(detalle_venta__idventa__fecha_hora=date.today()).annotate(total=Sum('detalle_venta__cantidad') * F('precio_venta')).values('nombre', 'detalle_venta__cantidad', 'total')

    return render(request, 'inicio.html',{'venta':venta})
#@login_required
#@group_required('GrupoUser')
def catalogo(request):
    productos = articulo.objects.annotate(cantidad=Sum('lote__cantidad_stock')).order_by('idarticulo')
    return render(request, 'catalogo.html',{'productos': productos})

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