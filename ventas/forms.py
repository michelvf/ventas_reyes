from django import forms
from .models import fileUpdate, Departamentos, Contador_billete, Lacteos, Cuenta
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
        self.fields['comentario'].widget = forms.Textarea(attrs={'class': 'form-control col-9', 'rows': 2, 'cols': 100})
    
    def _get_cuenta(self):
        try:
            return Cuenta.objects.get(cuenta='Efectivo')
        except Cuenta.DoesNotExist:
            return None
    
    def clean_un_peso(self):
        """
        Validador si se solicita más de $1 del que hay
        """
        valor = self.cleaned_data.get("un_peso")
        cuenta = self._get_cuenta()
        tipo_cuenta = self.cleaned_data.get("tipo_cuenta")

        if str(tipo_cuenta) == "Salida" and cuenta and valor > cuenta.un_peso:
            raise forms.ValidationError("❌ No tienes tantos billetes de $1 peso para dar.")

        return valor
    
    
    def clean_tres_pesos(self):
        """
        Validador si se solicita más de $3 del que hay
        """
        valor = self.cleaned_data.get("tres_pesos")
        cuenta = self._get_cuenta()
        tipo_cuenta = self.cleaned_data.get("tipo_cuenta")

        if str(tipo_cuenta) == "Salida" and cuenta and valor > cuenta.tres_pesos:
            raise forms.ValidationError("❌ No tienes tantos billetes de $3 pesos para dar.")

        return valor
    
    
    def clean_cinco_pesos(self):
        """
        Validador si se solicita más de $5 del que hay
        """
        valor = self.cleaned_data.get("cinco_pesos")
        cuenta = self._get_cuenta()
        tipo_cuenta = self.cleaned_data.get("tipo_cuenta")

        if str(tipo_cuenta) == 'Salida' and cuenta and valor > cuenta.cinco_pesos:
            raise forms.ValidationError("❌ No tienes tantos billetes de $5 pesos para dar.")

        return valor
    
    
    def clean_diez_pesos(self):
        """
        Validador si se solicita más de $10 del que hay
        """
        valor = self.cleaned_data.get("diez_pesos")
        cuenta = self._get_cuenta()
        tipo_cuenta = self.cleaned_data.get("tipo_cuenta")

        if str(tipo_cuenta) == 'Salida' and cuenta and valor > cuenta.diez_pesos:
            raise forms.ValidationError("❌ No tienes tantos billetes de $10 pesos para dar.")

        return valor

    
    def clean_veinte_pesos(self):
        """
        Validador si se solicita más de $20 del que hay
        """
        valor = self.cleaned_data.get("veinte_pesos")
        cuenta = self._get_cuenta()
        tipo_cuenta = self.cleaned_data.get("tipo_cuenta")

        if str(tipo_cuenta) == 'Salida' and cuenta and valor > cuenta.veinte_pesos:
            raise forms.ValidationError("❌ No tienes tantos billetes de $20 pesos para dar.")

        return valor
    
    
    def clean_cincuenta_pesos(self):
        """
        Validador si se solicita más de $50 del que hay
        """
        valor = self.cleaned_data.get("cincuenta_pesos")
        cuenta = self._get_cuenta()
        tipo_cuenta = self.cleaned_data.get("tipo_cuenta")

        if str(tipo_cuenta) == 'Salida' and cuenta and valor > cuenta.cincuenta_pesos:
            raise forms.ValidationError("❌ No tienes tantos billetes de $50 pesos para dar.")

        return valor
    
    
    def clean_cien_pesos(self):
        """
        Validador si se solicita más de $100 del que hay
        """
        valor = self.cleaned_data.get("cien_pesos")
        cuenta = self._get_cuenta()
        tipo_cuenta = self.cleaned_data.get("tipo_cuenta")

        if str(tipo_cuenta) == 'Salida' and cuenta and valor > cuenta.cien_pesos:
            raise forms.ValidationError("❌ No tienes tantos billetes de $100 pesos para dar.")

        return valor
    
    def clean_doscientos_pesos(self):
        """
        Validador si se solicita más de $200 del que hay
        """
        valor = self.cleaned_data.get("doscientos_pesos")
        cuenta = self._get_cuenta()
        tipo_cuenta = self.cleaned_data.get("tipo_cuenta")

        if str(tipo_cuenta) == 'Salida' and cuenta and valor > cuenta.doscientos_pesos:
            raise forms.ValidationError("❌ No tienes tantos billetes de $200 pesos para dar.")

        return valor
    
    
    def clean_quinientos_pesos(self):
        """
        Validador si se solicita más de $500 del que hay
        """
        valor = self.cleaned_data.get("quinientos_pesos")
        cuenta = self._get_cuenta()
        tipo_cuenta = self.cleaned_data.get("tipo_cuenta")

        if str(tipo_cuenta) == 'Salida' and cuenta and valor > cuenta.quinientos_pesos:
            raise forms.ValidationError("❌ No tienes tantos billetes de $500 pesos para dar.")

        return valor

    
    def clean_mil_pesos(self):
        """
        Validador si se solicita más de $1000 del que hay
        """
        valor = self.cleaned_data.get("mil_pesos")
        cuenta = self._get_cuenta()
        tipo_cuenta = self.cleaned_data.get("tipo_cuenta")

        if str(tipo_cuenta) == 'Salida' and cuenta and valor > cuenta.mil_pesos:
            raise forms.ValidationError("❌ No tienes tantos billetes de $1000 pesos para dar.")

        return valor
    
    # def clean(self):
    #     cleaned_data = super().clean()
    #     tipo_cuenta = cleaned_data.get("tipo_cuenta")
    #     un_peso = cleaned_data.get("un_peso")
    #     tres_pesos = cleaned_data.get("tres_pesos")
    #     cinco_pesos = cleaned_data.get("cinco_pesos")
    #     diez_pesos = cleaned_data.get("diez_pesos")
    #     veinte_pesos = cleaned_data.get("veinte_pesos")
    #     cincuenta_pesos = cleaned_data.get("cincuenta_peszos")
    #     cien_pesos = cleaned_data.get("dicie_pesos")
    #     doscientos_pesos = cleaned_data.get("doscientos_pesos")
    #     quinientos_pesos = cleaned_data.get("quinientos_pesos")
    #     mil_pesos = cleaned_data.get("mil_pesos")

    #     # Obtener el último histórico, por ejemplo
    #     try:
    #         cuenta = Cuenta.objects.get(cuenta='Efectivo')
    #     except Cuenta.DoesNotExist:
    #         return cleaned_data  # Si no hay histórico, no se puede comparar

    #     # errores = []

    #     if str(tipo_cuenta) == "Salida":
    #         if un_peso is not None and un_peso  > cuenta.un_peso :
    #             errores.append("No tienes tantos billetes de: uno peso, para dar.")
    #         if tres_pesos is not None and tres_pesos > cuenta.tres_pesos:
    #             errores.append("No tienes tantos billetes de: tres pesos, para dar.")
    #         if cinco_pesos is not None and cinco_pesos > cuenta.cinco_pesos:
    #             errores.append("No tienes tantos billetes de: cinco pesos, para dar.")
    #         if diez_pesos is not None and diez_pesos > cuenta.diez_pesos:
    #             errores.append("No tienes tantos billetes de: diez pesos, para dar.")
    #         if veinte_pesos is not None and veinte_pesos > cuenta.veinte_pesos:
    #             errores.append("No tienes tantos billetes de: veinte pesos, para dar.")
    #         if cincuenta_pesos is not None and cincuenta_pesos > cuenta.cincuenta_pesos:
    #             errores.append("No tienes tantos billetes de: cincuenta pesos, para dar.")
    #         if cien_pesos is not None and cien_pesos > cuenta.cien_pesos:
    #             errores.append("No tienes tantos billetes de: cien pesos, para dar.")
    #         if doscientos_pesos is not None and doscientos_pesos > cuenta.doscientos_pesos:
    #             errores.append("No tienes tantos billetes de: doscientos pesos, para dar.")
    #         if quinientos_pesos is not None and  quinientos_pesos > cuenta.quinientos_pesos:
    #             errores.append("No tienes tantos billetes de: quinientos pesos, para dar.")
    #         if mil_pesos is not None and mil_pesos > cuenta.mil_pesos:
    #             errores.append("No tienes tantos billetes de: mil pesos, para dar.")
                
    #     if errores:
    #         raise forms.ValidationError(errores)

    #     return cleaned_data


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