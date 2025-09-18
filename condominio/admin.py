from django.contrib import admin
from .models import (
    Rol,
    Casa,
    Perfil,
    AreaComun,
    Mascota,
    ConfiguracionGeneral,
    Reserva,
    Incidente,
    Invitacion,
    Comunicado,
    Expensas,
)


admin.site.register(Rol)
admin.site.register(Casa)
admin.site.register(Perfil)
admin.site.register(AreaComun)
admin.site.register(Mascota)
admin.site.register(ConfiguracionGeneral)
admin.site.register(Reserva)
admin.site.register(Incidente)
admin.site.register(Invitacion)
admin.site.register(Comunicado)
admin.site.register(Expensas)
