from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum, F, Q
from .models import articulo, lote

# Create your views here.

def login(request):
    return render(request, 'login.html',{
        'form': AuthenticationForm
    })

def group_required(GrupoAdmin):
    def check_group(RobertoJ):
        return RobertoJ.groups.filter(name=GrupoAdmin).exists()
    return user_passes_test(check_group)

def group_required(GrupoUser):
    def check_group(vendedor1):
        return vendedor1.groups.filter(name=GrupoUser).exists()
    return user_passes_test(check_group)

@login_required
@group_required('GrupoAdmin')
def inicioAdmin(request):
    datos = articulo.objects.annotate(total_cantidad=Sum('lote__cantidad_stock'), fecha_ven=F('lote__fecha_vencimiento')).order_by('idarticulo') 
    return render(request, 'inicioAdmin.html',{'datos': datos})
@login_required
@group_required('GrupoAdmin')
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
@group_required('GrupoAdmin')
def ventas(request):
    return render(request, 'agregarProducto.html',{})

@login_required
@group_required('GrupoUser')
def inicio(request):
    return render(request, 'inicio.html',{})
@login_required
@group_required('GrupoUser')
def catalogo(request):
    return render(request, 'catalogo.html',{})
