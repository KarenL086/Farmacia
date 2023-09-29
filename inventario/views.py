from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum, F, Q, Prefetch, DecimalField
from .models import articulo, lote, detalle_ingreso, venta, detalle_venta
from .forms import ArticuloForm, LoteForm, VentaForm, DetalleVentaForm,VentaDetalleForm
from datetime import date #, SesionForm
import json

# Create your views here.
# def listar(request):

    

#     return render(request, 'ventas/crearVenta.html', context)

def login(request):
    return render(request, 'login.html',{
        'form': AuthenticationForm
    })
#Metodo de verificacion
# def vistaLog(request):
#     if request.method == 'POST':
#         username= request.POST['username']
#         password= request.POST['password']
#         user = authenticate(request, username=username,password=password)
#         if user is not None:
#             login(request, user) # type: ignore
#             if user.groups.filter(name='GrupoAdmin').exists(): # type: ignore
#                 return redirect('inicioAdmin')
#             elif user.groups.filter(name='GrupoUser').exists(): # type: ignore
#                 return redirect('inicio')
#             return render(request, 'login.html', {'error': 'Nombre de usuario o contraseña incorrectos'})
#         else:
#             return render(request, 'login.html')


def group_required1(GrupoAdmin):
    def check_group(User):
        return User.groups.filter(name=GrupoAdmin).exists()
    return user_passes_test(check_group)

def group_required(GrupoUser):
    def check_group(User):
        return User.groups.filter(name=GrupoUser).exists()
    return user_passes_test(check_group)

@login_required
@group_required1('GrupoAdmin')
def inicioAdmin(request):
    venta= articulo.objects.filter(detalle_venta__idventa__fecha_hora=date.today()).annotate(total=Sum('detalle_venta__cantidad') * F('precio_venta'), cantidad=F('detalle_venta__cantidad')).values('nombre', 'cantidad', 'total')
    pocos = articulo.objects.annotate(cantidad=Sum('lote__cantidad_stock')).filter(Q(cantidad__lte=5) | Q(cantidad__lte=5)).order_by('cantidad')
    
    return render(request, 'inicioAdmin.html',{'venta':venta, 'pocos':pocos})

@login_required
@group_required1('GrupoAdmin')
def inventario(request):
    productos = articulo.objects.annotate(nlote=F('lote__lote'), fecha_ven=F('lote__fecha_vencimiento'), compra=F('lote__precio_compra'), cantidad=F('lote__cantidad_stock') ).order_by('fecha_ven')
    pocos = articulo.objects.annotate(cantidad=Sum('lote__cantidad_stock')).filter(Q(cantidad__lte=5) | Q(cantidad__lte=5)).order_by('cantidad')
    return render(request, 'inventario.html',{'productos': productos , 'pocos':pocos})

@login_required
@group_required1('GrupoAdmin')
def ventas(request):
    ventas= articulo.objects.annotate(fecha=F('detalle_venta__idventa__fecha_hora'),total=Sum('detalle_venta__cantidad') * F('precio_venta'), cantidad=F('detalle_venta__cantidad'), iddetalle=F('detalle_venta__iddetalle_venta'), costo=F('lote__precio_compra'), ganancia=(F('precio_venta')-F('lote__precio_compra'))*F('detalle_venta__cantidad')).values('nombre', 'precio_venta','costo', 'cantidad', 'total','ganancia', 'iddetalle', 'fecha')
    return render(request,'agregarProducto.html',{'ventas':ventas})

def searchv(request):
    q=request.GET["q"]
    ventas = articulo.objects.annotate(fecha=F('detalle_venta__idventa__fecha_hora'), total=Sum('detalle_venta__cantidad') * F('precio_venta'), cantidad=F('detalle_venta__cantidad'), iddetalle=F('detalle_venta__iddetalle_venta'), costo=F('lote__precio_compra'), ganancia=(F('precio_venta')-F('lote__precio_compra'))*F('detalle_venta__cantidad')).values('nombre', 'precio_venta','costo', 'cantidad', 'total','ganancia', 'iddetalle', 'fecha').filter(nombre__icontains=q)
    return render(request,'agregarProducto.html',{'ventas':ventas})


    # articulo_list = articulo.objects.all()
    # lote_list = lote.objects.all()
    # venta_list = venta.objects.all()
    # detalle_venta_list = detalle_venta.objects.all()
    

    # # Unir las listas en una sola lista de diccionarios
    # data_list = []
    # for articulo_obj, lote_obj, venta_obj, detalle_venta_obj in zip(articulo_list, lote_list, venta_list, detalle_venta_list):
    #     costo_compra = articulo_obj.precio_venta  # Supongamos que el costo de compra está en el modelo Articulo
    #     precio_venta = lote_obj.precio_compra
    #     ganancia = precio_venta - costo_compra
    #     data_list.append({

    #         'articulo': articulo_obj,
    #         'lote': lote_obj,
    #         'venta': venta_obj,
    #         'detalle_venta': detalle_venta_obj,
    #         'ganancia': ganancia,
            
    #     })

    # context = {
    #     'data_list': data_list,  # Pasamos la lista combinada a la plantilla
    # }

    # return render(request, 'agregarProducto.html', context)

# def ventas(request):
#     objeto_list = list(articulo.objects.all()) + list(lote.objects.all())+ list(venta.objects.all())+list(detalle_venta.objects.all())
#     context = {
        
#         'objeto_list': objeto_list,
#     }
#     return render(request, 'agregarProducto.html',context)




@login_required
@group_required('GrupoUser')
def inicio(request):
    venta= articulo.objects.filter(detalle_venta__idventa__fecha_hora=date.today()).annotate(total=Sum('detalle_venta__cantidad') * F('precio_venta'), cantidad=F('detalle_venta__cantidad')).values('nombre', 'cantidad', 'total')
    pocos = articulo.objects.annotate(cantidad=Sum('lote__cantidad_stock')).filter(Q(cantidad__lte=5) | Q(cantidad__lte=5)).order_by('cantidad')
    return render(request, 'inicio.html',{'venta':venta, 'pocos':pocos})

@login_required
@group_required('GrupoUser')
def catalogo(request):
    productos = articulo.objects.annotate(cantidad=Sum('lote__cantidad_stock')).order_by('idarticulo')
    return render(request, 'catalogo.html',{'productos': productos})

def search(request):
    q=request.GET["q"]
    productos = articulo.objects.filter(nombre__icontains=q)
    return render(request,'catalogo.html',{'productos': productos})

def search2(request):
    q=request.GET["q"]
    productos = articulo.objects.annotate(nlote=F('lote__lote'), fecha_ven=F('lote__fecha_vencimiento'), compra=F('lote__precio_compra'), cantidad=F('lote__cantidad_stock') ).order_by('fecha_ven').filter(nombre__icontains=q)
    return render(request,'inventario.html',{'productos': productos})


def asignarLote(request):
    if request.method == 'POST':
        formulario2 = LoteForm(data=request.POST)
        
        if formulario2.is_valid():
            lote1 = formulario2.save(commit=False)
            articulo1 = articulo.objects.get(idarticulo=request.POST['idarticulo'])
            stockcantidad= request.POST.get('cantidad_stock')
            lote1.idarticulo = articulo1
            lote1.cantidad_stock = stockcantidad  
            lote1.save()
            return redirect(to="inventario")
    else: 
        formulario2 = LoteForm()

    return render(request, 'medicina/asignarLote.html', {'formulario2': formulario2})


def crear(request):
    data = {
        'form': ArticuloForm()
    }
    if request.method == 'POST':
        formulario = ArticuloForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="asignarLote")
        else: 
            data['form'] = formulario

    return render(request, 'medicina/crear.html', data)


def modificar_articulo_lote(request, id):
    articulo_lote = get_object_or_404(articulo, idarticulo=id)
    lote_obj = get_object_or_404(lote, idarticulo=articulo_lote)

    if request.method == 'POST':
        articulo_form = ArticuloForm(request.POST, instance=articulo_lote, files=request.FILES)
        lote_form = LoteForm(request.POST, instance=lote_obj)

        if articulo_form.is_valid() and lote_form.is_valid():
            articulo_form.save()
            lote_form.save()
            return redirect('inventario')

    else:
        articulo_form = ArticuloForm(instance=articulo_lote)
        lote_form = LoteForm(instance=lote_obj)

    return render(request, 'medicina/editar_articulo_lote.html', {'articulo_form': articulo_form, 'lote_form': lote_form})


def eliminar(request, id):
    art = get_object_or_404(articulo, idarticulo=id)
    art.delete()
    return redirect(to="inventario")



#CRUD VENTAS

def crearVenta(request):
    data = {
        'form': VentaForm()
    }
    if request.method == 'POST':
        venta1 = VentaForm(data=request.POST)
        if venta1.is_valid():
            venta1.save()
            return redirect(to="crearDetalleVenta")
        else: 
            data['form'] = venta1
    return render(request, 'ventas/crearVenta.html', data)

def crearDetalleVenta(request):
    data = {
        'form': DetalleVentaForm()
    }
    if request.method == 'POST':
        dventa1 = DetalleVentaForm(data=request.POST)
        if dventa1.is_valid():
            dventa1.save()
            return redirect(to="ventas")
        else: 
            data['form'] = dventa1
    return render(request, 'ventas/detalleVenta/crearDV.html', data)



def editarVenta(request, id):
    venta_instance = get_object_or_404(venta, pk=id)
    detalle_venta_instance = detalle_venta.objects.filter(idventa=venta_instance)

    if request.method == 'POST':
        venta_form = VentaForm(request.POST, instance=venta_instance)
        detalle_venta_form = VentaDetalleForm(request.POST)

        if venta_form.is_valid() and detalle_venta_form.is_valid():
            venta_form.save()
            detalle_venta_obj = detalle_venta_form.save(commit=False)
            detalle_venta_obj.idventa = venta_instance
            detalle_venta_obj.save()
            

            return redirect('ventas')
    else:
        venta_form = VentaForm(instance=venta_instance)
        detalle_venta_form = VentaDetalleForm()

    return render(request, 'ventas/editarVenta.html', {
        'venta_form': venta_form,
        'detalle_venta_form': detalle_venta_form,
    })

def eliminarVenta(request, id):
    venta_instance = get_object_or_404(venta, pk=id)
    venta_instance.delete()
    return redirect('ventas')
