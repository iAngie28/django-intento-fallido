# models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    permisos = models.TextField(help_text="Lista de permisos separados por comas")
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"

class Casa(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    familia = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=20, choices=[
        ('ocupada', 'Ocupada'),
        ('libre', 'Libre'),
        ('mantenimiento', 'Mantenimiento')
    ], default='libre')
    area_m2 = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"Casa {self.codigo}"
    
    class Meta:
        verbose_name = "Casa"
        verbose_name_plural = "Casas"


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True)
    casa = models.ForeignKey(Casa, on_delete=models.SET_NULL, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    placa = models.CharField(max_length=10, unique=True,  blank=True, null=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    def es_copropietario(self):
        return self.rol and self.rol.nombre == "Copropietario"
    
    def es_administrador(self):
        return self.rol and self.rol.nombre == "Administrador"
    
    def es_guardia(self):
        return self.rol and self.rol.nombre == "Guardia"
    
    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"


class AreaComun(models.Model):
    nombre = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=[
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('mantenimiento', 'Mantenimiento')
    ], default='activo')
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Área Común"
        verbose_name_plural = "Áreas Comunes"



class Mascota(models.Model):
    nombre = models.CharField(max_length=50)
    raza = models.CharField(max_length=50)
    casa = models.ForeignKey(Casa, on_delete=models.CASCADE, related_name='mascotas')
    
    def __str__(self):
        return f"{self.nombre} - Casa {self.casa.codigo}"
    
    class Meta:
        verbose_name = "Mascota"
        verbose_name_plural = "Mascotas"



class ConfiguracionGeneral(models.Model):
    descuento_pago_anual = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        help_text="Porcentaje de descuento (ej: 10.50 para 10.5%)"
    )
    
    def __str__(self):
        return f"Descuento anual: {self.descuento_pago_anual}%"
    
    class Meta:
        verbose_name = "Configuración General"
        verbose_name_plural = "Configuración General"

class Reserva(models.Model):
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_salida = models.TimeField()
    area_comun = models.ForeignKey(AreaComun, on_delete=models.CASCADE, related_name='reservas')
    id_cop = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservas_solicitadas')
    id_adm = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservas_aprobadas')
    
    def __str__(self):
        return f"Reserva {self.area_comun.nombre} - {self.fecha}"
    
    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        unique_together = ['area_comun', 'fecha', 'hora_inicio']  # Evitar reservas duplicadas

class Incidente(models.Model):
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=[
        ('abierto', 'Abierto'),
        ('en_proceso', 'En Proceso'),
        ('resuelto', 'Resuelto'),
        ('cerrado', 'Cerrado')
    ], default='abierto')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    id_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='incidente_reportado')
    id_adm = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='incidente_resuelto')
    
    def __str__(self):
        return f"Incidente {self.id} - {self.id_user.username if self.id_user else 'Sin usuario'}"
    
    class Meta:
        verbose_name = "Incidente"
        verbose_name_plural = "Incidentes"

class Invitacion(models.Model):
    id_guardia = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='aprobado_por')
    casa = models.ForeignKey(Casa, on_delete=models.CASCADE, related_name='invitaciones')
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20)
    fecha_desde = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
        ('vencida', 'Vencida')
    ], default='pendiente')
    placa = models.CharField(max_length=10, blank=True)
    
    def __str__(self):
        return f"Invitación {self.nombre} - Casa {self.casa.codigo}"
    
    class Meta:
        verbose_name = "Invitación"
        verbose_name_plural = "Invitaciones"

# Comunicados se puede manejar en dos o varias tablas de manera independiente, lo puse asi para que cuando llegue el momento se vea como manejarlo.
class Comunicado(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    id_cop = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recibe_comunicado')
    id_adm = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='envia_comunicado')
    estado = models.CharField(max_length=20, choices=[
        ('visto', 'Visto'),
        ('no_Visto', 'No visto')
    ], default='no_Visto')

    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = "Comunicado"
        verbose_name_plural = "Comunicados"
        ordering = ['-fecha_creacion']

class Expensas(models.Model):
    id_cop = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='paga_expen')
    casa = models.ForeignKey(Casa, on_delete=models.CASCADE, related_name='expensas')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    mes = models.CharField(max_length=20)
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('pagada', 'Pagada'),
        ('vencida', 'Vencida')
    ], default='pendiente')
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ano = models.IntegerField()
    
    def __str__(self):
        return f"Expensas {self.mes}/{self.ano} - Casa {self.casa.codigo}"
    
    class Meta:
        verbose_name = "Expensa"
        verbose_name_plural = "Expensas"
        unique_together = ['casa', 'mes', 'ano']  # Una expensa por mes por casa

# Signals para crear automáticamente el perfil cuando se crea un usuario
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    if hasattr(instance, 'perfil'):
        instance.perfil.save()