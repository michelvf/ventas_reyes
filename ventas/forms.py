from django import forms
from .models import fileUpdate, Departamentos, Contador_billete, Lacteos
from django.core.validators import MinValueValidator


class ExcelUploadForm(forms.Form):
    """
    Class for upload Excel File
    """
    file = forms.FileField(
        label = 'Agregue el fichero a subir',
        widget=forms.FileInput(
            attrs={'class': 'form-control'}
        )
    )
    datefilter = forms.DateField(
        label='Escoja la fecha del fichero: '
    )
    actualizar = forms.BooleanField(
        label='',
        widget=forms.HiddenInput(),
        required=False,
    )


class DateRangeForm(forms.Form):
    """
    Form Class to date range 
    """
    start_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date'}
        )
    )
    end_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date'}
        )
    )


class UploadSQLFileForm(forms.Form):
    sql_file = forms.FileField(
        label='Fichero SQL'
        # widget=forms.FileField(
        #     attrs={'class': 'form-control'}
        # )
    )


class ArchivoExcelForm(forms.ModelForm):
    """
    Formulario para subir ficheros excel
    """
    # actualizar = forms.CheckboxInput()
    
    class Meta:
        model = fileUpdate
        fields = ['archivo', 'fecha']


class DepartamentosForm(forms.ModelForm):
    """
    Formulario para actualizar departamentos
    """
    class Meta:
        model = Departamentos
        fields = ['comentario', 'punto_de_venta']
        widgets = {
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'cols': 40, 'rows':2})
        }


class CalculadoraBilletesForm(forms.ModelForm):
    """
    Formulario para el registro del Cálculo
    """
    class Meta:
        model = Contador_billete
        fields = ['total', 'tipo_cuenta', 'un_peso', 'tres_pesos', 'cinco_pesos', 'diez_pesos', 'veinte_pesos', 'cincuenta_pesos', 'cien_pesos', 'doscientos_pesos', 'quinientos_pesos', 'mil_pesos', 'comentario']
        widgets = {
           "comentario": forms.Textarea(attrs={"class": "form-control col-9", "cols": 100, "rows": 4}),
           "total": forms.HiddenInput(attrs={"class": "disable"}),
        }
          
    def __init__(self, *args, **kwargs):
        super(CalculadoraBilletesForm, self).__init__(*args, **kwargs)
        # self.fields['total'].widget = forms.HiddenInput()
        self.fields['tipo_cuenta'].widget.attrs.update({'class': 'form-control col-9 entrada'})
        self.fields['un_peso'].widget.attrs.update({'class': 'form-control col-9 entrada bill-input', 'data-denomination': 1, 'value': 0, 'min': 0})
        self.fields['un_peso'].required = False
        self.fields['tres_pesos'].widget.attrs.update({'class': 'form-control col-9 entrada bill-input', 'data-denomination': 3, 'value': 0, 'min': 0})
        self.fields['tres_pesos'].required = False
        self.fields['cinco_pesos'].widget.attrs.update({'class': 'form-control col-9 entrada bill-input', 'data-denomination': 5, 'value': 0, 'min': 0})
        self.fields['cinco_pesos'].required = False
        self.fields['diez_pesos'].widget.attrs.update({'class': 'form-control col-9 entrada bill-input', 'data-denomination': 10, 'value': 0, 'min': 0})
        self.fields['diez_pesos'].required = False
        self.fields['veinte_pesos'].widget.attrs.update({'class': 'form-control col-9 entrada bill-input', 'data-denomination': 20, 'value': 0, 'min': 0})
        self.fields['veinte_pesos'].required = False
        self.fields['cincuenta_pesos'].widget.attrs.update({'class': 'form-control col-9 entrada bill-input', 'data-denomination': 50, 'value': 0, 'min': 0})
        self.fields['cincuenta_pesos'].required = False
        self.fields['cien_pesos'].widget.attrs.update({'class': 'form-control col-9 entrada bill-input', 'data-denomination': 100, 'value': 0, 'min': 0})
        self.fields['cien_pesos'].required = False
        self.fields['doscientos_pesos'].widget.attrs.update({'class': 'form-control col-9 entrada bill-input', 'data-denomination': 200, 'value': 0, 'min': 0})
        self.fields['doscientos_pesos'].required = False
        self.fields['quinientos_pesos'].widget.attrs.update({'class': 'form-control col-9 entrada bill-input', 'data-denomination': 500, 'value': 0, 'min': 0})
        self.fields['quinientos_pesos'].required = False
        self.fields['mil_pesos'].widget.attrs.update({'class': 'form-control col-9 entrada bill-input', 'data-denomination': 1000, 'value': 0, 'min': 0 })
        self.fields['mil_pesos'].required = False
        # self.fields['comentario'].widget = forms.Textarea(attrs={'class': 'form-control col-9', 'row': 4, 'cols': 100})
        
    # total = forms.IntegerField(
    #     widget=forms.HiddenInput(
    #         attrs={
    #             'class': 'disable',
    #         }
    #     )
    # )


class LacteosForm(forms.ModelForm):
    """
    Fromulario para los Láteos
    """
    class Meta:
        model = Lacteos
        fields = ['nombre', 'descripcion']
        widgets = {
            "nombre": forms.TextInput(attrs={"class":"form-control"}),
            "descripcion": forms.Textarea(attrs={"class":"form-control", "rows": 2  })
        }


class DondeSeVendeMasForm(forms.Form):
    """
    Formulario para lo más vendido
    """
    anno = forms.IntegerField()
    mes = forms.IntegerField()


class EstudioInventarioForm(forms.Form):
    """
    Formulario para subir ficheros excel
    """
    # actualizar = forms.CheckboxInput()
    
    ipv = forms.FileField(label="Subir Excel IPV")
    eleventa = forms.FileField(label="Subir Excel Eleventa")