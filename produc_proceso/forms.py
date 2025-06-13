from django import forms
from .models import Producto, Material, ProcesoProduccion, EntradaProduccion

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio_venta']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['nombre', 'descripcion', 'costo_unitario', 'unidad_medida']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

class ProcesoProduccionForm(forms.ModelForm):
    class Meta:
        model = ProcesoProduccion
        fields = ['producto', 'fecha_inicio', 'estado', 'notas']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'notas': forms.Textarea(attrs={'rows': 3}),
        }

class EntradaProduccionForm(forms.ModelForm):
    class Meta:
        model = EntradaProduccion
        fields = ['material', 'cantidad', 'fecha', 'notas']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'notas': forms.Textarea(attrs={'rows': 2}),
        }
