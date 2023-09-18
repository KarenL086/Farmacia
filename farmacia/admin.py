from django.contrib import admin
from . import models

@admin.register(models.articulo)
class TareaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_venta','descripcion',)
    search_fields = ('nombre',)

@admin.register(models.lote)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('lote', 'cantidad_stock',)
    search_fields = ('lote',)
