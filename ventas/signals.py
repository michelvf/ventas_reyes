from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cuenta, Cuenta_historico

@receiver(post_save, sender=Cuenta)
def duplicar_registro(sender, instance, **kwargs):
    """
    Cada vez que un Registro se guarde (insert o update),
    crear o actualizar su backup en RegistroBackup.
    """
    
    print('--------- estoy dentro de Signals')
    # print(f"--------- Lo que trae instancia Saldo: {instance.saldo}")
    # for p in instance:
    #    print(f"Lo que tiene instancia es: {p}")
    
    
    # backup, _ = Cuenta_historico.objects.create()
    backup = Cuenta_historico.objects.create()
    backup.un_peso = instance.un_peso
    backup.tres_pesos = instance.tres_pesos
    backup.cinco_pesos  = instance.cinco_pesos
    backup.diez_pesos = instance.diez_pesos
    backup.veinte_pesos = instance.veinte_pesos
    backup.cincuenta_pesos = instance.cincuenta_pesos
    backup.cien_pesos = instance.cien_pesos
    backup.doscientos_pesos = instance.doscientos_pesos
    backup.quinientos_pesos = instance.quinientos_pesos
    backup.mil_pesos = instance.mil_pesos
    backup.saldo = instance.saldo
    
    backup.save()
