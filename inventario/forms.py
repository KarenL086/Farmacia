from django import forms
from .models import articulo
from django.contrib.auth.forms import AuthenticationForm

class ArticuloForm(forms.ModelForm):
    class Meta:
        model = articulo
        fields= '__all__'

#Formulario
# class SesionForm(AuthenticationForm):
#     pass