from django.db import models

class articulo(models.Model):
    idarticulo=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=100, verbose_name='Producto')
    precio_venta = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Precio venta')
    descripcion = models.TextField(null=True, verbose_name='Descripcion')
    # imagen = models.ImageField(upload_to='imagenes/', null=true)

class lote(models.Model):
    idlote=models.AutoField(primary_key=True)
    idautor=models.ForeignKey(articulo)
    nombre=models.CharField(max_length=100, verbose_name='Lote')
    cantidad_stock=models.IntegerField()
    fecha_vencimiento=models.DateField()

class ingreso(models.Model):
    iddetalle_ingreso=models.AutoField(primary_key=True)
    proveedor=models.CharField(max_length=100)
    fecha=models.DateField()
    total=models.DecimalField(max_digits=5, decimal_places=2)

class detalle_ingreso(models.Model):
    iddetalle_ingreso=models.AutoField(primary_key=True)
    idingreso=models.ForeignKey(ingreso)
    idarticulo=models.ForeignKey(articulo)
    cantidad=models.IntegerField()
    precio=models.DecimalField(max_digits=5, decimal_places=2)

class venta(models.Model):
    idventa=models.AutoField(primary_key=True)
    fecha_hora=models.DateTimeField()
    total=models.DecimalField(max_digits=5, decimal_places=2)

class detalle_venta(models.Model):
    iddetalle_venta=models.AutoField(primary_key=True)
    idventa=models.ForeignKey(venta)
    idarticulo=models.ForeignKey(articulo)
    cantidad=models.IntegerField()
    precio=models.DecimalField(max_digits=5, decimal_places=2)
     