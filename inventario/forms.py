from django import forms
from .models import articulo, lote, venta, detalle_venta
from django.contrib.auth.forms import AuthenticationForm

class VentaForm(forms.ModelForm):
    class Meta:
        model = venta
        fields = '__all__'

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = detalle_venta
        fields = '__all__'
        
class ArticuloForm(forms.ModelForm):
    class Meta:
        model = articulo
        fields = '__all__'

class LoteForm(forms.ModelForm):
    class Meta:
        model = lote
        fields= '__all__'

        widgets = {
            "fecha_vencimiento": forms.SelectDateWidget()
        }
        

#Formulario
# class SesionForm(AuthenticationForm):
#     pass
