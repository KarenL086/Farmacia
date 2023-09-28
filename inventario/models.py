from django.db import models
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver

# Create your models here.
class articulo(models.Model):
    idarticulo=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=100, verbose_name='Producto')
    precio_venta = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Precio venta')
    descripcion = models.TextField(null=True, verbose_name='Descripcion')
    imagen = models.ImageField(upload_to='inventario/', blank=True)


    def __str__ (self): 
        return self.nombre


class lote(models.Model):
    idlote=models.AutoField(primary_key=True)
    idarticulo=models.ForeignKey(articulo, on_delete=models.CASCADE)
    lote=models.CharField(max_length=100, verbose_name='Lote')
    precio_compra=models.DecimalField(max_digits=5, decimal_places=2)
    cantidad_stock=models.IntegerField()
    fecha_vencimiento=models.DateField()
    def __str__(self): 
        return self.lote


class ingreso(models.Model):
    idingreso=models.AutoField(primary_key=True)
    proveedor=models.CharField(max_length=100)
    fecha=models.DateField(auto_now_add=True)
    total=models.DecimalField(max_digits=5, decimal_places=2)
    # def __str__(self):
    #     return str(self.idingreso)


class detalle_ingreso(models.Model):
    iddetalle_ingreso=models.AutoField(primary_key=True)
    idingreso=models.ForeignKey(ingreso, on_delete=models.CASCADE)
    idarticulo=models.ForeignKey(articulo, on_delete=models.CASCADE)
    cantidad=models.IntegerField()
    precio=models.DecimalField(max_digits=5, decimal_places=2)
    # def __str__(self):
    #     return str(self.iddetalle_ingreso)


class venta(models.Model):
    idventa=models.AutoField(primary_key=True)
    fecha_hora=models.DateField(auto_now_add=True)
    total=models.DecimalField(max_digits=5, decimal_places=2, default=0)
    # def __str__(self):
    #     return str(self.total)

    # @property
    # def total_price(self):
    #     cartitems = self.cartitems.all()
    #     total = sum([item.precio_venta for item in cartitems])
    #     return total
    
    # @property
    # def num_of_items(self):
    #     cartitems = self.cartitems.all()
    #     cantidad = sum([item.cantidad for item in cartitems])
    #     return cantidad

class detalle_venta(models.Model):
    iddetalle_venta=models.AutoField(primary_key=True)
    idventa=models.ForeignKey(venta, on_delete=models.CASCADE)
    idarticulo=models.ForeignKey(articulo, on_delete=models.CASCADE)
    cantidad=models.IntegerField(default=0)
    # def __str__(self): 
    #     return str(self.iddetalle_venta)
    
@receiver(post_save, sender=detalle_venta)
def correct_price(sender, **kwargs):
    cart_items = kwargs['instance']
    price_of_product = articulo.objects.get(cart_items.articulo.idarticulo)
    cart = detalle_venta.objects.filter(cart_items.idventa)
    cart.total = cart_items.articulo.precio_venta * cart_items.cantidad
    cart = venta.objects.get(cart_items.venta.idventa)
    cart.save()
    


