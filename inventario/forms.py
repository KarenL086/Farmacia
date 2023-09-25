from django import forms
from .models import articulo, lote

class ArticuloForm(forms.ModelForm):
    class Meta:
        model = articulo
        fields = '__all__'
        

class LoteForm(forms.ModelForm):
    class Meta:
        model = lote
        fields = ['idlote', 'idarticulo', 'lote', 'precio_compra','cantidad_stock', 'fecha_vencimiento']

        widgets = {
            "fecha_vencimiento": forms.SelectDateWidget()
        }
