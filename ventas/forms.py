from django import forms
from .models import fileUpdate

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