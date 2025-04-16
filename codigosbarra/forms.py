from django import forms


class CodigoBarrasForm(forms.Form):
    """
    Class for Bar Code data
    """
    codigo = forms.IntegerField(
        max_value=999999,
        min_value=0,
        required=True
    )
    nombre = forms.CharField(
        required=True
    )

class CodigosBarraExcelFrom(forms.Form):
    """
    Class for Bar Code Excel
    """
    file = forms.FileField(
        #label = 'Agregue el fichero a subir',
        # widget=forms.FileInput(
        #     attrs={'class': 'form-control'}
        # )
    )
    