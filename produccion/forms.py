from django import forms
from .models import Produccion, Salida, Categoria, Producto


class CategoriaForm(forms.ModelForm):
    """
    Formulario de Cliente, app Produccion
    """
    class Meta:
        model = Categoria
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ProduccionForm(forms.ModelForm):
    """
    Formulario de Producción, app Produccion
    """
    class Meta:
        model = Produccion
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }


class SalidaForm(forms.ModelForm):
    """
    Formulario de Salida, app Produccion
    """
    class Meta:
        model = Salida
        fields = ['producto', 'cantidad', 'destino']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'destino': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ProductoForm(forms.ModelForm):
    """
    Formulario de Producto, app Produccion
    """
    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'stock_actual']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'stock_actual': forms.NumberInput(attrs={'class': 'form-control'})
        }