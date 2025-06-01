from django import forms
from .models import Produccion, Salida, Categoria, Producto, Destino


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
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }


class SalidaForm(forms.ModelForm):
    """
    Formulario de Salida, app Produccion
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter products with stock_actual > 0
        self.fields['producto'].queryset = Producto.objects.filter(stock_actual__gt=0)
        
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        producto = self.cleaned_data.get('producto')
        
        if producto and cantidad:
            if cantidad < 1:
                raise forms.ValidationError("La cantidad debe ser mayor que 0")
            if cantidad > producto.stock_actual:
                raise forms.ValidationError(f"La cantidad no puede ser mayor al stock disponible ({producto.stock_actual})")
        
        return cantidad

    class Meta:
        model = Salida
        fields = ['producto', 'cantidad', 'destino']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'destino': forms.Select(attrs={'class': 'form-control'}),
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
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'stock_actual': forms.NumberInput(attrs={'class': 'form-control'})
        }


class DestinoForm(forms.ModelForm):
    """
    Formulario de Destino, app Produccion
    """
    class Meta:
        model = Destino
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }
