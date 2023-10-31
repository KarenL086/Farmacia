import re
from typing import Any
from django import forms
from .models import articulo, lote, venta, detalle_venta
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group
from django.forms import DateInput, ImageField, ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import PasswordChangeForm

class PNGImageField(ImageField):
    def to_python(self, data):
        f = super().to_python(data)
        if f is None:
            return None

        if f.content_type != 'image/png':
            raise ValidationError('Solo se permiten archivos PNG.')

        if f.size > 2097152:
            raise ValidationError('El tamaño máximo de archivo es de 2 MB.')

        return f
class VentaDetalleForm(forms.ModelForm):
    class Meta:
        model = detalle_venta
        exclude = ('idventa',)

class VentaForm(forms.ModelForm):
    fecha_hora=forms.DateField(widget=DateInput(attrs={'type':'date'}))
    class Meta:
        model = venta
        fields = '__all__'

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = detalle_venta
        fields = '__all__'
        
class ArticuloForm(forms.ModelForm):
    imagen = PNGImageField()
    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"]
        if not self.instance.pk:
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


class editarUsuario(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email','groups']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not self.instance.pk:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("El nombre de usuario ya existe.")
        return username


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Contraseña actual', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='Nueva contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Confirmar nueva contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        if len(password1) < 8:
            raise forms.ValidationError("La contraseña es muy corta")
        if not re.search(r'\d', password1):
            raise forms.ValidationError("La contraseña debe tener almenos un número")
        return password1

