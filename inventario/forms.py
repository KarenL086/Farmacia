from django import forms
from .models import articulo

class ArticuloForm(forms.ModelForm):
    class Meta:
        model = articulo
        fields= '__all__'