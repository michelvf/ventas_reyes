from django import forms
from .models import Cargo, DepartamentoNom, Trabajador, Nomina
from .models import Trabajador2, Nomina2
from django.utils import timezone


class CargoForm(forms.ModelForm):
    """
    Formulario para el Almacén
    """
    class Meta:
        model = Cargo
        fields = ['cargo', 'comentario', 'activo']
        # widget = {
        #     'comentario': forms.Textarea(attrs={'class': 'form-control'}),
        #     'cargo': forms.TextInput(attrs={'class': 'form-control'}),
        # }

    cargo = forms.CharField(
        max_length=255,
        label='Cargo:',
        widget=forms.TextInput(
            attrs={'class': 'form-control col-2'}
        )
    )

    comentario = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 4, 'class': 'form-control col-2'}
        )
    )

    activo = forms.BooleanField(
        widget=forms.CheckboxInput(
            # attr={'class': 'az-toggle az-toggle-success on'}
        )
    )


class TrabajadorForm(forms.ModelForm):
    """
    Formulario para los Trabajadores
    """
    class Meta:
        model = Trabajador
        fields = ['nombre', 'departamento', 'cargo', 'fecha']
        widgets = {
            'departamento': forms.Select(
                attrs={
                    'class': 'form-control select2-no-search select2-hidden-accessible col-2'
                }
            ),
            'cargo': forms.Select(
                attrs={
                    'class': 'form-control select2-no-search select2-hidden-accessible col-2'
                }
            ),
        }

    nombre = forms.CharField(
        max_length=255,
        label='Nombre:',
        widget=forms.TextInput(
            attrs={'class': 'form-control col-2'},
        )
    )

    fecha = forms.DateField(
        widget=forms.DateInput(
            format="%Y-%m-%d",
            # input_formats=["%d-%m-%Y"],
            attrs={
                'class': 'form-control col-2',
                'type': 'date',
                'value': timezone.now().strftime("%Y-%m-%d"),
            },
        )
    )


class NominaForm(forms.ModelForm):
    """
    Formulario para los Trabajadores
    """
    class Meta:
        model = Nomina
        fields = ['trabajador', 'salario', 'fecha']
        widgets = {
            'trabajador': forms.Select(
                attrs={
                    'class': 'form-control select2-no-search select2-hidden-accessible col-2'
                }
            ),
            # 'cargo': forms.Select(
            #     attrs={
            #         'class': 'form-control select2-no-search select2-hidden-accessible col-2'
            #     }
            # ),
        }

    # trabajador = forms.Select(
    #     widget=forms.ChoiceField(
    #         attrs={'class': 'form-control col-2'},
    #     )
    # )

    salario = forms.IntegerField(
        label='Salario:',
        widget=forms.NumberInput(
            attrs={'class': 'form-control col-2'}
        )
    )

    fecha = forms.DateField(
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={
                'class': 'form-control col-2',
                'type': 'date',
                'value': timezone.now().strftime("%Y-%m-%d"),
            },
        )
    )


class DepartamentoForm(forms.ModelForm):
    """
    Formulario para los Departamentos
    """
    class Meta:
        model = DepartamentoNom
        fields = ['departamento', 'comentario']
        
    departamento = forms.CharField(
        max_length=255,
        label='Nombre:',
        widget=forms.TextInput(
            attrs={'class': 'form-control col-2'},
        )
    )
    
    comentario = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 4, 'class': 'form-control col-2'}
        )
    )


class Trabajador2Form(forms.ModelForm):
    """
    Formulario para los Trabajadores 2
    """
    class Meta:
        model = Trabajador2
        fields = ['nombre', 'salario', 'fecha_entrada', 'activo', 'fecha_baja']
        # widgets = {
        #     'departamento': forms.Select(
        #         attrs={
        #             'class': 'form-control select2-no-search select2-hidden-accessible col-2'
        #         }
        #     ),
        #     'cargo': forms.Select(
        #         attrs={
        #             'class': 'form-control select2-no-search select2-hidden-accessible col-2'
        #         }
        #     ),
        # }

    nombre = forms.CharField(
        max_length=255,
        label='Nombre:',
        widget=forms.TextInput(
            attrs={'class': 'form-control col-2'},
        )
    )
    
    salario = forms.FloatField(
        label='Salario:',
        widget=forms.NumberInput(
            attrs={'class': 'form-control col-2'}
        )
    )

    fecha_entrada = forms.DateField(
        widget=forms.DateInput(
            format="%Y-%m-%d",
            # input_formats=["%d-%m-%Y"],
            attrs={
                'class': 'form-control col-2',
                'type': 'date',
                'value': timezone.now().strftime("%Y-%m-%d"),
            },
        )
    )
    
    activo = forms.BooleanField(
        widget=forms.CheckboxInput(
            # attr={'class': 'az-toggle az-toggle-success on'}
        ),
        required=False,
    )
    
    fecha_baja = forms.DateField(
        widget=forms.DateInput(
            format="%Y-%m-%d",
            # input_formats=["%d-%m-%Y"],
            attrs={
                'class': 'form-control col-2',
                'type': 'date',
                'value': "",
            },
        ),
        required=False,
    )


class NominaForm2(forms.ModelForm):
    """
    Formulario para los Trabajadores 2
    """
    class Meta:
        model = Nomina2
        fields = ['trabajador', 'fecha']
        widgets = {
            'trabajador': forms.Select(
                attrs={
                    'class': 'form-control select2-no-search select2-hidden-accessible col-2'
                }
            ),
            # 'cargo': forms.Select(
            #     attrs={
            #         'class': 'form-control select2-no-search select2-hidden-accessible col-2'
            #     }
            # ),
        }

    fecha = forms.DateField(
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={
                'class': 'form-control col-2',
                'type': 'date',
                'value': timezone.now().strftime("%Y-%m-%d"),
            },
        )
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo los objetos activos
        self.fields['trabajador'].queryset = Trabajador2.objects.filter(activo=True)

    # trabajador = forms.Select(
    #     widget=forms.ChoiceField(
    #         attrs={'class': 'form-control col-2'},
    #     )
    # )

