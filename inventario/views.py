from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum, F, Q
from datetime import datetime
from .models import articulo, lote, detalle_ingreso
from .forms import ArticuloForm, LoteForm

# Create your views here.

def login(request):
    return render(request, 'login.html',{
        'form': AuthenticationForm
    })

def group_required1(GrupoAdmin):
    def check_group(RobertoJ):
        return RobertoJ.groups.filter(name=GrupoAdmin).exists()
    return user_passes_test(check_group)

def group_required(GrupoUser):
    def check_group(vendedor1):
        return vendedor1.groups.filter(name=GrupoUser).exists()
    return user_passes_test(check_group)

@login_required
@group_required1('GrupoAdmin')
def inicioAdmin(request):
    datos = articulo.objects.annotate(total_cantidad=Sum('lote__cantidad_stock'), fecha_ven=F('lote__fecha_vencimiento')).order_by('idarticulo') 
    return render(request, 'inicioAdmin.html',{'datos': datos})
@login_required
@group_required1('GrupoAdmin')
def inventario(request):
    productos = articulo.objects.annotate(nlote=F('lote__lote'), fecha_ven=F('lote__fecha_vencimiento'), compra=F('lote__precio_compra')).order_by('fecha_ven')
    # queryset = request.GET.get('buscar')
    # if queryset:
    #     productos = Post.objects.filter(
    #         Q(nombre__icontains = queryset),
    #         Q(lote__icontains = queryset)
    #     )

    return render(request, 'inventario.html',{'productos': productos})
@login_required
@group_required1('GrupoAdmin')
def ventas(request):
    return render(request, 'agregarProducto.html',{})

@login_required
@group_required('GrupoUser')
def inicio(request):
    return render(request, 'inicio.html',{})
@login_required
@group_required('GrupoUser')
def catalogo(request):
    productos = articulo.objects.annotate(cantidad=Sum('lote__cantidad_stock')).order_by('idarticulo')
    return render(request, 'catalogo.html',{'productos': productos})

def asignarLote(request):
    if request.method == 'POST':
        formulario2 = LoteForm(data=request.POST)
        
        if formulario2.is_valid():
            lote1 = formulario2.save(commit=False)
            articulo1 = articulo.objects.get(idarticulo=request.POST['idarticulo'])
            lote1.idarticulo = articulo1
            lote1.cantidad_stock = 0  # Asegúrate de proporcionar un valor para 'cantidad_stock'
            lote1.save()
    else: 
        formulario2 = LoteForm()

    return render(request, 'medicina/asignarLote.html', {'formulario2': formulario2})


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

def modificar_producto(request, id):
    articuloX = get_object_or_404(articulo, idarticulo=id)

    data = {
        'form': ArticuloForm(instance=articuloX)
    }

    if request.method == 'POST':
        formulario3 = ArticuloForm(data=request.POST, instance=articuloX, files=request.FILES)
        if formulario3.is_valid():
            formulario3.save()
            return redirect(to="inventario")
        data['form']=formulario3
    return render(request, 'medicina/editar.html', data)