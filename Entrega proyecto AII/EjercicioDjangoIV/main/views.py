#encoding:utf-8
from main.models import RopaHombre
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from main.populateDB import extraer_ropaHombre, indexar_datos
import os 
from whoosh.index import create_in, open_dir
from main.forms import BusquedaRopaForm



def poblar_base_datos(request):
    try:
        extraer_ropaHombre()  
        messages.success(request, "La base de datos ha sido poblada correctamente.")
    except Exception as e:
        messages.error(request, f"Ocurrió un error: {e}")
    return redirect('pagina_inicio')

def indexar_datos(request):
    index_dir = "Index"
    
    if os.path.exists(index_dir):
        messages.warning(request, "El índice ya existe. ¿Está seguro de que quiere recargar los datos? Esta operación puede ser lenta.")
        
        if request.method == "POST":
            ix = open_dir(index_dir)
            writer = ix.writer()
            writer.commit()
            
            messages.success(request, "Datos recargados correctamente.")
            return redirect('pagina_inicio')
        else:
            return render(request, 'confirmar_recarga.html')

    else:
        os.makedirs(index_dir)
        ix = create_in(index_dir, schema) 
        writer = ix.writer()
        writer.commit()
        
        messages.success(request, "Índice creado y datos indexados correctamente.")
        return redirect('pagina_inicio')

def pagina_inicio(request):
    return render(request, 'pagina_inicio.html')

def lista_ropa_hombre(request):
    ropa_hombre = RopaHombre.objects.all()

    return render(request, 'lista_ropa_hombre.html', {'ropa_hombre': ropa_hombre})

def lista_ropa_hombre_rebajada(request):
    ropa_hombre_rebajada = RopaHombre.objects.exclude(descuento='')

    return render(request, 'lista_ropa_hombre.html', {'ropa_hombre': ropa_hombre_rebajada})


def buscar_ropa_hombre(request):
    form = BusquedaRopaForm(request.GET or None)
    ropa_hombre = RopaHombre.objects.all()

    if form.is_valid():
        query = form.cleaned_data['query']
        ropa_hombre = ropa_hombre.filter(nombre__icontains=query)

    return render(request, 'buscar_ropa_hombre.html', {'form': form, 'ropa_hombre': ropa_hombre})

def buscar_precio(request):
    precio_min = request.GET.get('precio_min', '')
    precio_max = request.GET.get('precio_max', '')
    
    if precio_min and precio_max:
        try:
            precio_min = float(precio_min.replace(',', '.').replace('€', '').strip())
            precio_max = float(precio_max.replace(',', '.').replace('€', '').strip())
            
            ropa_hombre = RopaHombre.objects.filter(precio__gte=precio_min, precio__lte=precio_max)
        except ValueError:
            ropa_hombre = []
            message = "Los precios deben estar en formato numérico."
            return render(request, 'lista_ropa_hombre.html', {'ropa_hombre': ropa_hombre, 'message': message})
    else:
        ropa_hombre = RopaHombre.objects.all()

    return render(request, 'lista_ropa_hombre.html', {'ropa_hombre': ropa_hombre})