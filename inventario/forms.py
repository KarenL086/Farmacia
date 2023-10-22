from typing import Any
from django import forms
from .models import articulo, lote, venta, detalle_venta
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group
from django.forms import DateInput, ValidationError
from django.contrib.auth.hashers import make_password

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
    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"]
        if articulo.objects.filter(nombre__iexact=nombre).exists():
            raise ValidationError("El artículo ya se encuentra registrado")
        return nombre
    
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



class RegistroUsuario(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'groups']


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not self.instance.pk:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("El nombre de usuario ya existe.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            return make_password(password)
        else:
            if not self.instance.pk:
                raise forms.ValidationError("La contraseña es obligatoria.")
            return self.instance.password


        # widgets = {
        #     'password': forms.PasswordInput
        # }
        #No se le ha agregado este widget debido a problemas para guardar la contraseña mientras se esta editando


