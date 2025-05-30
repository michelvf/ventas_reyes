from django.shortcuts import render
from .models import Trabajador, DepartamentoNom, Nomina, Cargo
from .models import Trabajador2, Nomina2
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views import View
from .forms import CargoForm, TrabajadorForm, NominaForm, DepartamentoForm, NominaForm2
from .forms import Trabajador2Form, NominaForm2
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from compras.forms import ResumenSemanal
from django.db.models import Sum, F


# Create your views here.

# ########## Listado #########
class DepartamentoList(ListView):
    """
    List of Departament
    """
    model = DepartamentoNom
    template_name = 'nomina/departamento_list.html'


class CargoList(ListView):
    """
    List of Departament
    """
    model = Cargo
    template_name = 'nomina/cargos_list.html'
    
    def get_queryset(self):
        """Return the last five published questions."""
        return Cargo.objects.filter(activo=True)
    
    # def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # context["URL"] = "/api/nomina_departamentos/"
        # context["Titulo"] = ""
        
        # return context


class TrabajdorList(ListView):
    """
    List of Departament
    """
    model = Trabajador
    template_name = 'nomina/trabajadores_list.html'
    
    # def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # context["URL"] = "/api/nomina_departamentos/"
        # context["Titulo"] = " | Trabajadores"
        
        # return context


class NominaList(ListView):
    """
    List of Payroll
    """
    template_name = 'nomina/nomina_list.html'
    model = Nomina
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["URL"] = "/api/nomina_departamentos/"
        # context["Titulo"] = " | Nómina"
        
        return context
    
    
class NominaList2(ListView):
    """
    List of Payroll 2
    """
    template_name = 'nomina/nomina_list2.html'
    model = Nomina2
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["URL"] = "/api/nomina_departamentos/"
        # context["Titulo"] = " | Nómina"
        
        return context

    
    def get_queryset(self):
        """Return the payroll ordering by date."""
        return Nomina2.objects.order_by("fecha")


class TrabajdorList2(ListView):
    """
    List of active worker 2
    """
    model = Trabajador2
    template_name = 'nomina/trabajadores_list2.html'
    
    # Mostrar todos los activos
    def get_queryset(self):
        return super().get_queryset().filter(
            activo=True
        ) # .annotate(
            # interviewed_number=Count('interviewer', filter=Q(interviewer__user__role='0', interviewer__is_approved=True))
        # )


class TrabajadorBaja(ListView):
    """
    List of out Worker
    """
    model = Trabajador2
    template_name = "nomina/bajas.html"
    
    # Show only out Worker
    def get_queryset(self):
        return super().get_queryset().filter(
            activo=False
        )


# ########### Agregar #############
class RegistrarCargosView(CreateView):
    """
    Register warehouses
    """
    model = Cargo
    form_class = CargoForm
    template_name = 'nomina/registrar_cargo.html'
    success_url = '/nomina/cargos/'
    # context_object_name = 'almacen'


    def get_success_url(self):
        if 'guardar_y_seguir' in self.request.POST:
            return reverse('registrar_cargo')
        else:
            return reverse('nomina_cargos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texto1"] = "Agregar un Cargo"
        context["texto2"] = "Se agrega un nuevo cargo."
        
        return context


class RegistrarTrabajadorView(CreateView):
    """
    Register Worked
    """
    model = Trabajador
    form_class = TrabajadorForm
    template_name = 'nomina/registrar_cargo.html'
    success_url = '/nomina/trabajadores/'

    def get_success_url(self):
        if 'guardar_y_seguir' in self.request.POST:
            return reverse('registrar_trabajador')
        else:
            return reverse('nomina_trabajadores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texto1"] = "Agregar un Trabajador"
        context["texto2"] = "Se agrega un nuevo trabajador."

        return context


class RegistrarNominaView(CreateView):
    """
    Register Payroll
    """
    model = Nomina
    form_class = NominaForm
    template_name = 'nomina/registrar_cargo.html'
    success_url = '/nomina/nomina/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texto1"] = "Agregar un trabajador a la Nómina"
        context["texto2"] = "Se agrega un nuevo trabajador con el salario que va a cobrar, en la nómina."

        return context

    def get_success_url(self):
        if 'guardar_y_seguir' in self.request.POST:
            return reverse('registrar_nomina')
        else:
            return reverse('nomina_list')


class RegistrarNominaView2(CreateView):
    """
    Register Payroll 2
    """
    model = Nomina2
    form_class = NominaForm2
    template_name = 'nomina/registrar_cargo2.html'
    success_url = '/nomina/nomina2/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texto1"] = "Agregar un trabajador a la Nómina"
        context["texto2"] = "Se agrega un nuevo trabajador con el salario que va a cobrar, en la nómina."

        return context

    def get_success_url(self):
        if 'guardar_y_seguir' in self.request.POST:
            return reverse('registrar_nomina2')
        else:
            return reverse('nomina_list2')



class RegistrarDepartamentoView(CreateView):
    """
    Register Departament
    """
    model = DepartamentoNom
    form_class = DepartamentoForm
    template_name = 'nomina/registrar_cargo.html'
    success_url = '/nomina/departamentos/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texto1"] = "Agregar un Departamento"
        context["texto2"] = "Se agrega un nuevo departamento a donde pertencerán los trabajadores."

        return context

    def get_success_url(self):
        if 'guardar_y_seguir' in self.request.POST:
            return reverse('registrar_departamento')
        else:
            return reverse('nomina_departamentos')


class RegistrarTrabajador2View(CreateView):
    """
    Register Worked 2
    """
    model = Trabajador2
    form_class = Trabajador2Form
    template_name = 'nomina/registrar_cargo2.html'
    success_url = '/nomina/trabajadores2/'

    def get_success_url(self):
        if 'guardar_y_seguir' in self.request.POST:
            return reverse('registrar_trabajador2')
        else:
            return reverse('nomina_trabajadores2')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texto1"] = "Agregar un Trabajador"
        context["texto2"] = "Se agrega un nuevo trabajador."

        return context


# class RegistrBajasView(CreateView):
#     """
#     Register Worked
#     """
#     model = Trabajador2
#     form_class = Trabajador2Form
#     template_name = 'nomina/registro_bajas.html'
#     success_url = '/nomina/trabajadores2/'

#     def get_success_url(self):
#         if 'guardar_y_seguir' in self.request.POST:
#             return reverse('registrar_bajas')
#         else:
#             return reverse('nomina_trabajadores2')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["texto1"] = "Agregar un Bajas"
#         context["texto2"] = "Se visualiza las bajas."

#         return context



# ########### Actualizar ##########
class ActualizarCargo(UpdateView):
    """
    Update the records
    """
    model = Cargo
    # fields = ["cargo", "comentario", "activo"]
    # template_name_suffix = "_update"
    template_name = 'nomina/editar_nomina.html'
    success_url = reverse_lazy('nomina_cargos')
    form_class = CargoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texto1"] = "Actualizar el Cargo"
        context["texto2"] = "Se actualiza la información del Cargo."

        return context


class ActualizarNomina(UpdateView):
    """
    Update the records
    """
    model = Nomina
    # fields = ['trabajador', 'salario', 'fecha', 'activo']
    form_class = NominaForm
    # template_name_suffix = "_update"
    template_name = 'nomina/editar_nomina.html'
    success_url = reverse_lazy('nomina_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texto1"] = "Actualizar la Nómina"
        context["texto2"] = "Se actualiza la información de la Nómina."
        
        return context
    

class ActualizarTrabajador(UpdateView):
    """
    Update the records
    """
    model = Trabajador
    # fields = ['nombre', 'departamento', 'cargo', 'fecha', 'activo']
    form_class = TrabajadorForm
    # template_name_suffix = "_update"
    template_name = 'nomina/editar_nomina.html'
    success_url = reverse_lazy('nomina_trabajadores')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texto1"] = "Actualizar el Trabajador"
        context["texto2"] = "Se actualiza la información del Trabajador."
        
        return context
    
    
class ActualizarDepartamento(UpdateView):
    """
    Register Departament
    """
    model = DepartamentoNom
    form_class = DepartamentoForm
    template_name = 'nomina/editar_nomina.html'
    success_url = reverse_lazy('nomina_departamentos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texto1"] = "Agregar un Departamento"
        context["texto2"] = "Se agrega un nuevo departamento a donde pertencerán los trabajadores."

        return context


class ActualizarTrabajador2(UpdateView):
    """
    Update the records worder 2
    """
    model = Trabajador2
    # fields = ['nombre', 'departamento', 'cargo', 'fecha', 'activo']
    form_class = Trabajador2Form
    # template_name_suffix = "_update"
    template_name = 'nomina/editar_nomina2.html'
    success_url = reverse_lazy('nomina_trabajadores2')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texto1"] = "Actualizar el Trabajador"
        context["texto2"] = "Se actualiza la información del Trabajador."
        
        return context


class ActualizarBaja(UpdateView):
    """
    Update the terminate a worker
    """
    model = Trabajador2
    # fields = ['nombre', 'departamento', 'cargo', 'fecha', 'activo']
    form_class = Trabajador2Form
    # template_name_suffix = "_update"
    template_name = 'nomina/editar_baja.html'
    success_url = reverse_lazy('nomina_trabajadores2')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texto1"] = "Actualizar la baja"
        context["texto2"] = "Se actualiza la información del Trabajador."
        
        return context


###### Consultas ######
class NominaDePagoView(View):
    """
    The Payroll by dates
    """
    def get(self, request):
        nomina_rango_fechas = None
        return render(
            request,
            'nomina/nomina_de_pago.html', 
            {'nomina_rango_fechas': nomina_rango_fechas}
            )
        
    def post(self, request):
        form = ResumenSemanal(request.POST)
        nomina_rango_fechas = None
        # print(f"Lo que llega del formulario POST: {form}")
        if form.is_valid():
            llega = form.cleaned_data['datefilter']
            
            # Separar las fechas
            fecha_informal= llega.split(' - ')
            # print(f"Fecha informal: {fecha_informal}")
            desde= fecha_informal[0]
            hasta = fecha_informal[1]
            
            # Hacer la consultas con el rango de fechas
            nomina_rango_fechas = Nomina.objects.filter(
                fecha__range=[desde, hasta]
            ).order_by('fecha')
            # print(f"Resume es: {nomina_rango_fechas} y de tamaño: {len(nomina_rango_fechas)}")
            # print()
            
            # Hacer un arreglo con las fechas
            fechas = []
            for f in nomina_rango_fechas:
                if f.fecha not in fechas:
                    fechas.append(f.fecha)
            # print(f"fechas es = {fechas}")
            
            # Inicia variables
            listado = []
            fila = {}
            cant = 0
            canti = []
            nombre = []
            comparar = True
            
            # Comenzado a iterar en el arreglo de la consulta de rango de fechas
            for l in nomina_rango_fechas:
                # Comprobar si los nombres no se repiten
                if l.trabajador not in nombre:
                    nombre.append(l.trabajador)
                    fila['nombre'] = l.trabajador.nombre
                    f = 0
                    
                    # Volviendo a recorre el arreglo para obtener el salarios
                    # de los trabajadores por los días trabajados
                    for p in nomina_rango_fechas:
                        if l.trabajador == p.trabajador:
                            # print('voy dentro del While')
                            while comparar:
                                # print(f"Comparando {p.trabajador} si fechas[f] {fechas[f]} == p.fecha: {p.fecha}")
                                if fechas[f] == p.fecha:
                                    canti.append(p.salario)
                                    cant += p.salario
                                    # print(f"coinciden fechas, el día: {fechas[f]} el trabajador: {p.trabajador.nombre} ganó: {p.salario}")
                                    comparar = False
                                else:
                                    canti.append(0)
                                    # print(f"no coinciden,  el día: {fechas[f]} el trabajador: {p.trabajador.nombre} no ganó nada")
                                    f += 1
                            f += 1
                            comparar = True
                            # canti.append(p.cantidad)
                            # cant += p.cantidad
                            
                    if len(fechas) != f:
                        canti.append(0)
                    
                    # print(f"se va a agregar a la fila:, canti tiene valores: {canti} y de tamaño: {len(canti)}")
                    
                    if len(canti) != len(fechas):
                        canti.append(0)
                        
                    fila['cantidad'] = canti
                    # print(f" f se quedó en: {f} y tamaño fechas {len(fechas)}")
                    canti = []
                    if cant != 0:
                        fila['cant'] = cant
                        listado.append(fila)
                        # print(f"para {l.trabajador.nombre}, se agrega la fila: {fila}")
                fila = {}
                cant = 0

            salarios_dias = (Nomina.objects.filter(fecha__range=[desde, hasta])
                .values('fecha')
                .annotate(
                    salarios=Sum(F'salario'),
                    #gasto_total=Sum(F('cantidad') * F('precio_compra'))
                )
                .order_by('fecha'))
            
            total_a_pagar = 0
            for n in salarios_dias:
                total_a_pagar += n['salarios']
            
        # print(f"salarios_dias es: {salarios_dias}")
        return render(
            request,
            'nomina/nomina_de_pago.html', 
            {
                'nomina_rango_fechas': nomina_rango_fechas,
                'fechas': fechas,
                'listado': listado,
                # 'totales_apagar': totales_apagar,
                'salarios_dias': salarios_dias,
                'total_a_pagar': total_a_pagar,
            }
        )


###### Consultas ######
class NominaDePagoView2(View):
    """
    The Payroll by dates 2
    """
    def get(self, request):
        nomina_rango_fechas = None
        return render(
            request,
            'nomina/nomina_de_pago2.html', 
            {'nomina_rango_fechas': nomina_rango_fechas}
            )
        
    def post(self, request):
        form = nomina_rango_fechasSemanal(request.POST)
        nomina_rango_fechas = None
        # print(f"Lo que llega del formulario POST: {form}")
        if form.is_valid():
            llega = form.cleaned_data['datefilter']
            
            # Separar las fechas
            fecha_informal= llega.split(' - ')
            # print(f"Fecha informal: {fecha_informal}")
            desde= fecha_informal[0]
            hasta = fecha_informal[1]
            
            # Hacer la consultas con el rango de fechas
            nomina_rango_fechas = Nomina2.objects.filter(
                fecha__range=[desde, hasta]
            ).order_by('fecha')
            # print(f"Resume es: {nomina_rango_fechas} y de tamaño: {len(nomina_rango_fechas)}")
            # print()
            
            # Hacer un arreglo con las fechas
            fechas = []
            for f in nomina_rango_fechas:
                if f.fecha not in fechas:
                    fechas.append(f.fecha)
            # print(f"fechas es = {fechas}")
            
            # Inicia variables
            listado = []
            fila = {}
            cant = 0
            canti = []
            nombre = []
            comparar = True
            
            # Comenzado a iterar en el arreglo de la consulta de rango de fechas
            for l in nomina_rango_fechas:
                # Comprobar si los nombres no se repiten
                if l.trabajador not in nombre:
                    nombre.append(l.trabajador)
                    fila['nombre'] = l.trabajador.nombre
                    f = 0
                    
                    # Volviendo a recorre el arreglo para obtener el salarios
                    # de los trabajadores por los días trabajados
                    for p in nomina_rango_fechas:
                        if l.trabajador == p.trabajador:
                            # print('voy dentro del While')
                            while comparar:
                                # print(f"Comparando {p.trabajador} si fechas[f] {fechas[f]} == p.fecha: {p.fecha}")
                                if fechas[f] == p.fecha:
                                    canti.append(p.salario)
                                    cant += p.salario
                                    # print(f"coinciden fechas, el día: {fechas[f]} el trabajador: {p.trabajador.nombre} ganó: {p.salario}")
                                    comparar = False
                                else:
                                    canti.append(0)
                                    # print(f"no coinciden,  el día: {fechas[f]} el trabajador: {p.trabajador.nombre} no ganó nada")
                                    f += 1
                            f += 1
                            comparar = True
                            # canti.append(p.cantidad)
                            # cant += p.cantidad
                            
                    if len(fechas) != f:
                        canti.append(0)
                    
                    # print(f"se va a agregar a la fila:, canti tiene valores: {canti} y de tamaño: {len(canti)}")
                    
                    if len(canti) != len(fechas):
                        canti.append(0)
                        
                    fila['cantidad'] = canti
                    # print(f" f se quedó en: {f} y tamaño fechas {len(fechas)}")
                    canti = []
                    if cant != 0:
                        fila['cant'] = cant
                        listado.append(fila)
                        # print(f"para {l.trabajador.nombre}, se agrega la fila: {fila}")
                fila = {}
                cant = 0

            salarios_dias = (Nomina2.objects.filter(fecha__range=[desde, hasta])
                .values('fecha')
                .annotate(
                    salarios=Sum(F'salario'),
                    #gasto_total=Sum(F('cantidad') * F('precio_compra'))
                )
                .order_by('fecha'))
            
            total_a_pagar = 0
            for n in salarios_dias:
                total_a_pagar += n['salarios']
            
        # print(f"salarios_dias es: {salarios_dias}")
        return render(
            request,
            'nomina/nomina_de_pago.html', 
            {
                'nomina_rango_fechas': nomina_rango_fechas,
                'fechas': fechas,
                'listado': listado,
                # 'totales_apagar': totales_apagar,
                'salarios_dias': salarios_dias,
                'total_a_pagar': total_a_pagar,
            }
        )