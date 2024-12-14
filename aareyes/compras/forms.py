from django import forms
from .models import Compra, Almacen, Producto, PrecioProducto


class AlmacenForm(forms.ModelForm):
    """
    Formulario para el Almacén
    """
    class Meta:
        model = Almacen
        fields = ['nombre']

    nombre = forms.CharField(
        max_length=255,
        label='Nombre:',
        widget=forms.TextInput(
            attrs={'class': 'form-control col-2'}
        )
    )


class ProductoForm(forms.ModelForm):
    """
    Formulario para los Productos
    """
    class Meta:
        model = Producto
        fields = ['nombre', 'almacen']

    nombre = forms.CharField(
        max_length=255,
        label='Nombre:',
        widget=forms.TextInput(
            attrs={'class': 'form-control col-2'}
        )
    )

    almacen = forms.ModelChoiceField(
        label='Almacen:',
        widget=forms.Select(
            attrs={'class': 'form-control col-2'}
        ),
        queryset=Almacen.objects.all(),
        empty_label="--- Escoger ---",
    )

    # widgets = {
    #     'nombre': forms.TextInput(attrs={'class': 'form-class',}),
    #     'almacen': forms.Select(attrs={'class': 'form-control col-3'}),
    # }

class PrecioProductoForm(forms.ModelForm):
    """
    Formulario para los Precios-Productos
    """
    class Meta:
        model = PrecioProducto
        fields = ['producto', 'precio']

    # widgets = {
    #     'precio': forms.NumberInput(
    #         attrs={
    #             'class': 'form-control',
    #         }
    #     )
    # }


    producto = forms.ModelChoiceField(
        label='Producto:',
        widget=forms.Select(
            attrs={'class': 'form-control col-2'}
        ),
        queryset=Producto.objects.all(),
        empty_label="--- Escoger ---",
    )
    
    precio = forms.IntegerField(
        label='Precio',
        widget=forms.NumberInput(
            attrs={'class': 'form-control col-2', 'step': 0.01}
        )
    )


class CompraForm(forms.ModelForm):
    """
    Formulario para las Compras
    """
    class Meta:
        model = Compra
        fields = ['producto', 'cantidad' , 'precio_compra']

    producto = forms.ModelChoiceField(
        label='Producto',
        widget=forms.Select(
            attrs={'class': 'form-control col-2',}
        ),
        queryset=Producto.objects.all(),
        empty_label='--- Escoger ---',
    )

    cantidad = forms.IntegerField(
        label='Cantidad',
        widget=forms.NumberInput(
            attrs={'class': 'form-control col-2',}
        )
    )

    precio_compra = forms.IntegerField(
        label='Precio de compra',
        widget=forms.NumberInput(
            attrs={'class': 'form-control col-2'}
        )
    )


