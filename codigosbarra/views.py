from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.views import View
# from barcode.writer import ImageWriter
from .forms import CodigoBarrasForm, CodigosBarraExcelFrom
from django.conf import settings
import os
import barcode

# Create your views here.

class barcode(View):
    """
    Página del formulario
    """
    template_name = 'codigosbarra/codigo.html'
    form = CodigoBarrasForm
    
    
    def get(self, request):
        return render(request, self.template_name)
    
    
    def post(self, request):
        form = CodigoBarrasForm(request.POST)
        if form.is_valid():
            cod = str(form.cleaned_data["codigo"])
            nombre = form.cleaned_data["nombre"]
            texto = cod + "-"+ nombre
            # barcode_type = "Gs1_128"
            # barcode_class = barcode.get_barcode_class(barcode_type)
            # my_barcode = barcode_class(texto, writer=ImageWriter())
            # url = settings.MEDIA_ROOT + '/ficheros/' + texto
            # file = my_barcode.save(url)
            
            render(request, self.template_name, {'file': file})
        else:
            print("no sidvió")    
        return render(request, self.template_name, {'form': form})


class generaruno(View):
    """
    Generar solo un código cuando se mande el formulario
    """
    template_name = 'codigosbarra/codigo.html'
    
    #def get(self, request):
    #    return True
    
    def post(self, request):
        
        
        return True

class fecheroExcel(View):
    """
    Generar Códigos de Barra a partir del fichero Excel del Abarrote/Eleventas
    """
    
    def get(self, request):
        return True
    
    def post(self, request):
        True
        