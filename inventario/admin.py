from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(articulo)
admin.site.register(lote)
admin.site.register(venta)
admin.site.register(detalle_venta)
