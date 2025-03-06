from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.views import View
import barcode
from barcode.writer import ImageWriter
import os

# Create your views here.

class barcode(TemplateView):
    """
    Página del formulario
    """
    template_name = 'codigosbarra/codigo.html'


class generaruno(View):
    """
    Generar solo un código cuando se mande el formulario
    """
    def get(request):
        return True
    
    def post(request):
        return True

