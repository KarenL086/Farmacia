from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum, F, Q, Prefetch, DecimalField
from .carrito import Carrito
from django.contrib.auth.models import User, Group
from .models import articulo, lote, venta, detalle_venta
from .forms import ArticuloForm, LoteForm, VentaForm, DetalleVentaForm,VentaDetalleForm,RegistroUsuario, editarUsuario, CustomPasswordChangeForm
from datetime import date
import json
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models.functions import Round
from django.views.decorators.cache import cache_control
# Create your views here.

    
def group_required1(GrupoAdmin):
    def check_group(User):
        return User.groups.filter(name=GrupoAdmin).exists()
    return user_passes_test(check_group)

def group_required(GrupoUser):
    def check_group(User):
        return User.groups.filter(name=GrupoUser).exists()
    return user_passes_test(check_group)

#VERIFICACION
def login(request):
    return render(request, 'login.html',{
        'form': AuthenticationForm
    })
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
@group_required1('GrupoAdmin')
def administrar_users(request):
    users = User.objects.all()
    return render(request, 'admin_users/administrar_users.html', {'users': users})
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuario(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('administrar_users')
    else:
        form = RegistroUsuario()
    return render(request, 'admin_users/registrar_usuario.html', {'form': form})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def editar_usuario(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = editarUsuario(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('administrar_users')
    else:
        form = editarUsuario(instance=user)
    return render(request, 'admin_users/editar_usuario.html', {'form': form})
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def change_password(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = CustomPasswordChangeForm(data=request.POST, user=user)
        if form.is_valid():
            form.save()
            return redirect('administrar_users')
    else:
        form = CustomPasswordChangeForm(user)
        print('No funciona')
    return render(request, 'admin_users/change_password.html', {'form': form})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def eliminar_usuario(request, user_id):
    user = User.objects.get(id=user_id)
    if request.user == user:
        return HttpResponse("""
            <script type="text/javascript">
                alert("No puedes eliminar tu propio usuario");
                window.location.href = "/administrar_users/";
            </script>
        """, content_type="text/html")
    user.delete()
    return redirect('administrar_users')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def inicioAdmin(request):
    venta= articulo.objects.filter(detalle_venta__idventa__fecha_hora=date.today()).annotate(total=F('detalle_venta__cantidad') * F('precio_venta'), cantidad=F('detalle_venta__cantidad')).values('nombre', 'cantidad', 'total', 'precio_venta')
    pocos = articulo.objects.annotate(cantidad=Sum('lote__cantidad_stock')).filter(Q(cantidad__lte=5) | Q(cantidad__lte=5)).order_by('cantidad')
    actual = date.today()
    vencidos = date.today() + timezone.timedelta(days=5)
    vencimiento = lote.objects.filter(fecha_vencimiento__lte=vencidos)
    return render(request, 'inicioAdmin.html',{'venta':venta, 'pocos':pocos, 'vencimiento':vencimiento,'actual':actual})
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
@group_required1('GrupoAdmin')
def inventario(request):
    productos = articulo.objects.annotate(nlote=F('lote__lote'), fecha_ven=F('lote__fecha_vencimiento'), compra=F('lote__precio_compra'), cantidad=F('lote__cantidad_stock') ).order_by('fecha_ven')
    pocos = articulo.objects.annotate(cantidad=Sum('lote__cantidad_stock')).filter(Q(cantidad__lte=5) | Q(cantidad__lte=5)).order_by('cantidad')
    actual = date.today()
    vencidos = date.today() + timezone.timedelta(days=5)
    vencimiento = lote.objects.filter(fecha_vencimiento__lte=vencidos)
    return render(request, 'inventario.html',{'productos': productos , 'pocos':pocos, 'vencimiento':vencimiento, 'actual':actual})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
@group_required1('GrupoAdmin')
def ventas(request):
    ventas = articulo.objects.annotate(total=F('detalle_venta__cantidad')*F('precio_venta'),cantidad=F('detalle_venta__cantidad'),fecha_hora=F('detalle_venta__idventa__fecha_hora'),idventa=F('detalle_venta__idventa'),iddetalle_venta=F('detalle_venta__iddetalle_venta'),ganancias=Round((F('lote__precio_compra')-(F('precio_venta')*F('detalle_venta__cantidad')))/F('lote__precio_compra'), 3)).values('fecha_hora','nombre','precio_venta','cantidad','total','iddetalle_venta','idventa','ganancias')
    ganancias_totales = detalle_venta.objects.annotate(total_por_articulo=F('idarticulo__precio_venta') * F('cantidad')).aggregate(total=Sum('total_por_articulo'))['total']
    ganancias_hoy = detalle_venta.objects.filter(idventa__fecha_hora=date.today()).annotate(total_por_articulo=F('idarticulo__precio_venta') * F('cantidad')).aggregate(total=Sum('total_por_articulo'))['total']
    if ganancias_hoy is None:
        ganancias_hoy = 00.00
    if ganancias_totales is None:
        ganancias_totales = 0.00
    return render(request,'agregarProducto.html',{'ventas':ventas,'ganancias_totales':ganancias_totales,'ganancias_hoy':ganancias_hoy})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def searchv(request):
    q=request.GET["q"]
    ventas = articulo.objects.annotate(total=F('detalle_venta__cantidad')*F('precio_venta'),cantidad=F('detalle_venta__cantidad'),fecha_hora=F('detalle_venta__idventa__fecha_hora'),idventa=F('detalle_venta__idventa'),iddetalle_venta=F('detalle_venta__iddetalle_venta'),ganancias=Round((F('lote__precio_compra')-(F('precio_venta')*F('detalle_venta__cantidad')))/F('lote__precio_compra'), 3)).values('fecha_hora','nombre','precio_venta','cantidad','total','iddetalle_venta','idventa','ganancias').filter(nombre__icontains=q)
    ganancias_totales = detalle_venta.objects.annotate(total_por_articulo=F('idarticulo__precio_venta') * F('cantidad')).aggregate(total=Sum('total_por_articulo'))['total']
    ganancias_hoy = detalle_venta.objects.filter(idventa__fecha_hora=date.today()).annotate(total_por_articulo=F('idarticulo__precio_venta') * F('cantidad')).aggregate(total=Sum('total_por_articulo'))['total']
    if ganancias_hoy is None:
        ganancias_hoy = 00.00
    if ganancias_totales is None:
        ganancias_totales = 0.00
    return render(request,'agregarProducto.html',{'ventas':ventas,'ganancias_totales':ganancias_totales,'ganancias_hoy':ganancias_hoy})

@login_required
#@group_required1('GrupoAdmin')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@group_required('GrupoUser')
def catalogo(request):
    productos = articulo.objects.annotate(cantidad=Sum('lote__cantidad_stock')).order_by('idarticulo').filter(cantidad__gt=0)
    return render(request, 'catalogo.html',{'productos': productos})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def search(request):
    q=request.GET["q"]
    productos = articulo.objects.filter(nombre__icontains=q)
    return render(request,'catalogo.html',{'productos': productos})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def search2(request):
    q=request.GET["q"]
    productos = articulo.objects.annotate(nlote=F('lote__lote'), fecha_ven=F('lote__fecha_vencimiento'), compra=F('lote__precio_compra'), cantidad=F('lote__cantidad_stock') ).order_by('fecha_ven').filter(nombre__icontains=q)
    return render(request,'inventario.html',{'productos': productos})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def eliminar(request, id):
    art = get_object_or_404(articulo, idarticulo=id)
    art.delete()
    return redirect(to="inventario")



#CRUD VENTAS
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def crearDetalleVenta(request):
    data = {
        'form': DetalleVentaForm()
    }

    if request.method == 'POST':
        dventa1 = DetalleVentaForm(data=request.POST)

        if dventa1.is_valid():
            detalle_venta = dventa1.save(commit=False)
            id_articulo = detalle_venta.idarticulo.idarticulo
            cantidad_vendida = detalle_venta.cantidad
            lto = lote.objects.get(idarticulo=id_articulo)

            if lto.cantidad_stock >= cantidad_vendida:
                detalle_venta.save()
                lto.cantidad_stock -= cantidad_vendida
                lto.save()
                return redirect(to="ventas")
            else:
                return HttpResponse("""
            <script type="text/javascript">
                alert("No hay suficientes elementos en stock ");
                window.location.href = "/crearDetalleVenta/";
            </script>
        """, content_type="text/html")
        else:
            data['form'] = dventa1

    return render(request, 'ventas/detalleVenta/crearDV.html', data)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editarVenta(request, idventa, iddetalle_venta):
    venta_instance = get_object_or_404(venta, idventa=idventa)
    detalle_venta_instance = get_object_or_404(detalle_venta, iddetalle_venta=iddetalle_venta)

    if request.method == 'POST':
        venta_form = VentaForm(request.POST, instance=venta_instance)
        detalle_venta_form = VentaDetalleForm(request.POST, instance=detalle_venta_instance)

        if venta_form.is_valid() and detalle_venta_form.is_valid():
            venta_form.save()
            detalle_venta_obj = detalle_venta_form.save(commit=False)
            detalle_venta_obj.idventa = venta_instance
            detalle_venta_obj.save()
            

            return redirect('ventas')
    else:
        venta_form = VentaForm(instance=venta_instance)
        detalle_venta_form = VentaDetalleForm(instance=detalle_venta_instance)

    return render(request, 'ventas/editarVenta.html', {
        'venta_form': venta_form,
        'detalle_venta_form': detalle_venta_form,
    })

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def eliminarVenta(request, id):
    venta_instance = get_object_or_404(venta, detalle_venta=id)
    venta_instance.delete()
    return redirect('ventas')

#Ventas y carrito
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def agregar_producto(request, idarticulo):
    carrito = Carrito(request)
    producto = articulo.objects.get(idarticulo=idarticulo)
    intentario= articulo.objects.annotate(cantidad=Sum('lote__cantidad_stock')).get(idarticulo=idarticulo)
    cantidad = int(intentario.cantidad)
    carrito.agregar(producto, cantidad)
    url_anterior = request.META.get('HTTP_REFERER')
    return  redirect(url_anterior)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def eliminar_producto(request, idarticulo):
    carrito = Carrito(request)
    producto = articulo.objects.get(idarticulo=idarticulo)
    carrito.eliminar(producto)
    url_anterior = request.META.get('HTTP_REFERER')
    return  redirect(url_anterior)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def restar_producto(request, idarticulo):
    carrito=Carrito(request)
    producto = articulo.objects.get(idarticulo=idarticulo)
    carrito.restar(producto)
    url_anterior = request.META.get('HTTP_REFERER')
    return  redirect(url_anterior)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    url_anterior = request.META.get('HTTP_REFERER')
    return  redirect(url_anterior)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def guardar_datos(request):
    carrito = Carrito(request)
    ve=venta()
    ve.fecha_hora=datetime.now()
    ve.total=0.00
    ve.save()
    for id_articulo, datos in carrito.carrito.items():
        dv=detalle_venta()
        dv.idventa=ve
        dv.idarticulo=articulo.objects.get(idarticulo=id_articulo)
        dv.cantidad=datos["cantidad"]
        dv.save()
        lt=lote()
        l = lote.objects.get(idarticulo=id_articulo)
        cantidad = int(l.cantidad_stock)
        l.cantidad_stock = (cantidad - datos["cantidad"])
        l.save()       
    carrito.limpiar()
    url_anterior = request.META.get('HTTP_REFERER')
    return  redirect(url_anterior)

#Errores
def error_404(request, exception):
    return render(request, 'errores/404.html', {})

def error_500(request):
    return render(request, 'errores/500.html', {})
