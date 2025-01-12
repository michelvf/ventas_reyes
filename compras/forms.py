from django import forms
from .models import Compra, Almacen, Producto, PrecioProducto, UnidadMedida
from django.utils import timezone

# from easy_select2 import select2_modelform, Select2, apply_select2


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
        fields = ['nombre', 'medida', 'almacen', 'imagen']

    nombre = forms.CharField(
        max_length=255,
        label='Nombre:',
        widget=forms.TextInput(
            attrs={'class': 'form-control col-2'}
        )
    )

    medida = forms.ModelChoiceField(
        label='Unidad de Medida:',
        widget=forms.Select(
            attrs={'class': 'form-control col-2'}
        ),
        queryset = UnidadMedida.objects.all(),
        empty_label="--- Escoger ---",
    )

    almacen = forms.ModelChoiceField(
        label='Almacen:',
        widget=forms.Select(
            attrs={'class': 'form-control col-2'}
        ),
        queryset=Almacen.objects.all(),
        empty_label="--- Escoger ---",
    )

    imagen = forms.FileField(
        label='Imagen:',
        widget=forms.ClearableFileInput(
            attrs={'class': 'form-control col-2'}
        ),
        required=False
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
        fields = ['producto', 'cantidad' , 'precio_compra', 'fecha']
        # widget = {
        #     'producto': apply_select2(forms.Select),
        #     'class': 'form-control',
        # }

    producto = forms.ModelChoiceField(
        label='Productores',
        widget=forms.Select(
            attrs={
                'class': 'form-control col-12 col-md-6',
                # 'onChange': 'select(this.value)'
            }
        ),
        queryset=Producto.objects.all(),
        empty_label='--- Escoger ---',
    )

    cantidad = forms.IntegerField(
        label='Cantidad',
        widget=forms.NumberInput(
            attrs={'class': 'form-control col-12 col-md-6',}
        )
    )

    precio_compra = forms.IntegerField(
        label='Precio de compra',
        widget=forms.NumberInput(
            attrs={'class': 'form-control col-12 col-md-6'}
        )
    )

    fecha = forms.DateTimeField(
        #initial=timezone.now(),
        label='Fecha:',
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput( 
            attrs={'class': 'form-control col-12 col-md-6', 'type': 'date'},
            format="%Y-%m-%d"
        )
    )


class ResumenSemanal(forms.Form):
    """
    Formulario para recibir el rago de fechas
    """
    # start_date = forms.DateField()
    # end_date = forms.DateField()
    datefilter = forms.CharField()
