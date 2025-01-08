from django import forms
from .models import Producto, Envio, Venta, Cliente, Proveedor
from .models import Categoria, Almacen, PuntoDeVenta


class ProductoForm(forms.ModelForm):
    """
    Formulario para Producto
    """
    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'proveedor', 'precio', 'cantidad']


class EnvioForm(forms.ModelForm):
    """
    Formulario para Envio
    """
    class Meta:
        model = Envio
        fields = ['almacen', 'producto', 'punto_de_venta', 'cantidad']
        widgets = {
            'producto': forms.Select(
                attrs={
                    'class': 'form-control select2-no-search select2-hidden-accessible col-2'
                }
            ),
            'almacen': forms.Select(
                attrs={
                    'class': 'form-control select2-no-search select2-hidden-accessible col-2'
                }
            ),
            'punto_de_venta': forms.Select(
                attrs={
                    'class': 'form-control select2-no-search select2-hidden-accessible col-2'
                }
            ),
            'cantidad': forms.NumberInput(
                attrs={
                    'class': 'form-control col-2'
                }
            )
        }
        
        # cantidad = forms.IntegerField(
        #     label='Salario:',
        #     widget=forms.NumberInput(
        #         attrs={'class': 'form-control col-2'}
        #     )
        # )


class VentaForm(forms.ModelForm):
    """
    Formulario para Venta
    """
    class Meta:
        model = Venta
        fields = ['producto', 'punto_de_venta', 'cantidad', 'total']


class ClienteForm(forms.ModelForm):
    """
    Formulario para Cliente
    """
    class Meta:
        model = Cliente
        fields = ['nombre', 'descripcion']
    
    nombre = forms.CharField(
        max_length=255,
        label='Nombre:',
        widget=forms.TextInput(
            attrs={'class': 'form-control col-2'},
        )
    )
    
    descripcion = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 4, 'class': 'form-control col-2'}
        )
    )


class ProveedorForm(forms.ModelForm):
    """
    Formulario para Proveedor
    """
    class Meta:
        model = Proveedor
        fields = ['nombre', 'contacto', 'direccion', 'telefono', 'correo']

    nombre = forms.CharField(
        max_length=255,
        label='Nombre:',
        widget=forms.TextInput(
            attrs={'class': 'form-control col-2'},
        )
    )
    
    contacto = forms.CharField(
        max_length=255,
        label='Contacto:',
        widget=forms.TextInput(
            attrs={'class': 'form-control col-2'},
        )
    )
    
    direccion = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 4, 'class': 'form-control col-2'}
        )
    )
    
    telefono = forms.CharField(
        max_length=255,
        label='Teléfono:',
        widget=forms.NumberInput(
            attrs={'class': 'form-control col-2', 'type': 'tel'},
        )
    )

    correo = forms.CharField(
        max_length=255,
        label='Correo:',
        widget=forms.EmailInput(
            attrs={'class': 'form-control col-2'},
        )
    )


class CategoriaForm(forms.ModelForm):
    """
    Formulario para Categoria
    """
    class Meta:
        model = Categoria
        fields = ['nombre']


class AlmacenForm(forms.ModelForm):
    """
    Formulario para Almacen
    """
    class Meta:
        model = Almacen
        fields = ['nombre', 'direccion']
    
    nombre = forms.CharField(
        max_length=255,
        label='Nombre:',
        widget=forms.TextInput(
            attrs={'class': 'form-control col-2'},
        )
    )
    
    direccion = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 4, 'class': 'form-control col-2'}
        )
    )


class PuntoDeVentaForm(forms.ModelForm):
    """
    Formulario para PuntoDeVenta
    """
    class Meta:
        model = PuntoDeVenta
        fields = ['nombre', 'direccion']
    
    nombre = forms.CharField(
        max_length=255,
        label='Nombre:',
        widget=forms.TextInput(
            attrs={'class': 'form-control col-2'},
        )
    )
    
    direccion = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 4, 'class': 'form-control col-2'}
        )
    )
