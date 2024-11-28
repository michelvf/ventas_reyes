from django import forms


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
        label='Escoja la fecha del fichero'
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
