from django import forms
from .models import Compra, Almacen, Producto, PrecioProducto, UnidadMedida
from .models import Cliente, Producto, Factura, DetalleFactura
from django.utils import timezone

# from easy_select2 import select2_modelform, Select2, apply_select2


class AlmacenForm(forms.ModelForm):
    """
    Formulario para el Almacén de Facturación
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


# class ProductosForm(forms.ModelForm):
#     """
#     Formulario para los Productos viejo
#     """
#     class Meta:
#         model = Producto
#         fields = ['nombre', 'medida', 'almacen']

#     nombre = forms.CharField(
#         max_length=255,
#         label='Nombre:',
#         widget=forms.TextInput(
#             attrs={'class': 'form-control col-2'}
#         )
#     )

#     medida = forms.ModelChoiceField(
#         label='Unidad de Medida:',
#         widget=forms.Select(
#             attrs={'class': 'form-control col-2'}
#         ),
#         queryset = UnidadMedida.objects.all(),
#         empty_label="--- Escoger ---",
#     )

#     almacen = forms.ModelChoiceField(
#         label='Almacen:',
#         widget=forms.Select(
#             attrs={'class': 'form-control col-2'}
#         ),
#         queryset=Almacen.objects.all(),
#         empty_label="--- Escoger ---",
#     )

    # imagen = forms.FileField(
    #     label='Imagen:',
    #     widget=forms.ClearableFileInput(
    #         attrs={'class': 'form-control col-2'}
    #     ),
    #     required=False
    # )

    # widgets = {
    #     'nombre': forms.TextInput(attrs={'class': 'form-class',}),
    #     'almacen': forms.Select(attrs={'class': 'form-control col-3'}),
    # }


class PrecioProductoForm(forms.ModelForm):
    """
    Formulario para los Precios-Productos de Facturación
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
    datefilter = forms.CharField()


class ClienteForm(forms.ModelForm):
    """
    Formulario para Cliente de Facturación
    """
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'ci', 'direccion', 'telefono', 'email']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            # 'documento': forms.TextInput(attrs={'class': 'form-control'}),
            'ci': forms.NumberInput(attrs={'class': 'form-control', 'pattern': '\d{11}', 'minlength': '11', 'maxlength': '11'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class ProductoForm(forms.ModelForm):
    """
    Formulario para el Producto de Facturación
    """
    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'descripcion', 'precio', 'unidadmedida']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'unidad de medida': forms.Select(attrs={'class': 'form-select'})
            # 'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class FacturaForm(forms.ModelForm):
    """
    Forumario para la Factura
    """
    class Meta:
        model = Factura
        fields = ['cliente', 'observaciones']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class DetalleFacturaForm(forms.ModelForm):
    """
    Formulario para el Detalle de la Factura
    """
    class Meta:
        model = DetalleFactura
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

# Formulario para el conjunto de detalles (formset)
DetalleFacturaFormSet = forms.inlineformset_factory(
    Factura, DetalleFactura,
    form=DetalleFacturaForm,
    extra=1, can_delete=True,
    min_num=1, validate_min=True
)