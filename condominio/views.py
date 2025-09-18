from django.shortcuts import get_object_or_404, redirect, render
from .form import CMascotaADM
from .models import Mascota

# Create your views here.
def create_mascota(request):
    if request.method == 'GET':
        return render(request, 'mascota/crear.html', {
            'form': CMascotaADM
        })
    else:
        form = CMascotaADM(request.POST)
        mascota = form.save(commit = False)
        mascota.save()
        return redirect('list_mascota')  
    
def list_mascota(request):
    masc = Mascota.objects.all()
    return render(request, 'mascota/list.html', {'mascotas': masc})

def show_mascota(request, pk):
    if request.method == 'GET':
        mascota = get_object_or_404(Mascota, pk=pk)
        form = CMascotaADM(instance=mascota)
        return render(request, 'mascota/detalles.html',  {'mascota': mascota, 'form': form})
    else:        
        mascota = get_object_or_404(Mascota, pk=pk)
        form = CMascotaADM(request.POST, instance=mascota)
        form.save()
        return redirect('list_mascota')
    
def eliminar_Mascota(request,pk):
    mascota = get_object_or_404(Mascota, pk=pk)
    if request.method == 'POST':
        mascota.delete()
    return redirect('list_mascota')