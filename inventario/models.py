from decimal import Decimal
from django.db import models
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver

# Create your models here.
class articulo(models.Model):
    idarticulo=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=100, verbose_name='Producto')
    precio_venta = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Precio de venta')
    descripcion = models.TextField(null=True, verbose_name='Descripcion')
    imagen = models.ImageField(upload_to='inventario/', blank=True)


    def __str__ (self): 
        return f'{self.nombre} -> {self.precio_venta}'


class lote(models.Model):
    idlote=models.AutoField(primary_key=True)
    idarticulo=models.ForeignKey(articulo, on_delete=models.CASCADE, verbose_name='Producto')
    lote=models.CharField(max_length=100, verbose_name='Lote')
    precio_compra=models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Precio de compra')
    cantidad_stock=models.IntegerField(verbose_name='Cantidad en stock')
    fecha_vencimiento=models.DateField(verbose_name='Fecha de vencimiento')
    def __str__(self): 
        return self.lote


class venta(models.Model):
    idventa=models.AutoField(primary_key=True)
    fecha_hora=models.DateField()
    def __str__(self):
        return str(self.idventa)

class detalle_venta(models.Model):
    iddetalle_venta=models.AutoField(primary_key=True)
    idventa=models.ForeignKey(venta, on_delete=models.CASCADE)
    idarticulo=models.ForeignKey(articulo, on_delete=models.CASCADE, verbose_name='Producto')
    cantidad=models.IntegerField(default=0)
    def __str__(self): 
        return str(self.iddetalle_venta)
    
    


