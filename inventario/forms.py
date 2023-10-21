from django import forms
from .models import articulo, lote, venta, detalle_venta
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group
from django import forms
from django.forms import DateInput, TimeInput


class VentaDetalleForm(forms.ModelForm):
    class Meta:
        model = detalle_venta
        exclude = ('idventa',)

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
    fecha_vencimiento = forms.DateField(
        widget=DateInput(
            attrs={'type': 'date'}
        )
    )
    class Meta:
        model = lote
        fields = '__all__'