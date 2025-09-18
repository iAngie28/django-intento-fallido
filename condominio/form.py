from django.forms import ModelForm
from condominio import models

class CMascotaADM (ModelForm):
    class Meta:
        model = models.Mascota
        fields = ['nombre', 'raza', 'casa']