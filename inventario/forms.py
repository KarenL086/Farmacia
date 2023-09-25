from django import forms
from .models import articulo, lote
from .models import articulo
from django.contrib.auth.forms import AuthenticationForm

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
        fields= '__all__'

#Formulario
# class SesionForm(AuthenticationForm):
#     pass
