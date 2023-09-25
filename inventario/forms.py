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
        fields= '__all__'

        widgets = {
            "fecha_vencimiento": forms.SelectDateWidget()
        }
        

#Formulario
# class SesionForm(AuthenticationForm):
#     pass
