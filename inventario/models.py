from django.db import models

# Create your models here.
class articulo(models.Model):
    idarticulo=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=100, verbose_name='Producto')
    precio_venta = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Precio venta')
    descripcion = models.TextField(null=True, verbose_name='Descripcion')
    imagen = models.ImageField(upload_to='imagenes/', blank=True)

class lote(models.Model):
    idlote=models.AutoField(primary_key=True)
    idarticulo=models.ForeignKey(articulo, on_delete=models.CASCADE)
    lote=models.CharField(max_length=100, verbose_name='Lote')
    precio_compra=models.DecimalField(max_digits=5, decimal_places=2)
    cantidad_stock=models.IntegerField()
    fecha_vencimiento=models.DateField()

class ingreso(models.Model):
    idingreso=models.AutoField(primary_key=True)
    proveedor=models.CharField(max_length=100)
    fecha=models.DateField()
    total=models.DecimalField(max_digits=5, decimal_places=2)
def __str__(self):
    return self.idingreso


class detalle_ingreso(models.Model):
    iddetalle_ingreso=models.AutoField(primary_key=True)
    idingreso=models.ForeignKey(ingreso, on_delete=models.CASCADE)
    idarticulo=models.ForeignKey(articulo, on_delete=models.CASCADE)
    cantidad=models.IntegerField()
    precio=models.DecimalField(max_digits=5, decimal_places=2)
def __str__(self):
    return self. iddetalle_ingreso


class venta(models.Model):
    idventa=models.AutoField(primary_key=True)
    fecha_hora=models.DateField()
    total=models.DecimalField(max_digits=5, decimal_places=2)
def __str__(self):
    return self.idventa


class detalle_venta(models.Model):
    iddetalle_venta=models.AutoField(primary_key=True)
    idventa=models.ForeignKey(venta, on_delete=models.CASCADE)
    idarticulo=models.ForeignKey(articulo, on_delete=models.CASCADE)
    cantidad=models.IntegerField()
def __str__(self):
    return self.iddetalle_venta
