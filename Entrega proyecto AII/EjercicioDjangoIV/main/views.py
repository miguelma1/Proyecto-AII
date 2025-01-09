#encoding:utf-8
from main.models import RopaHombre
from main.populateDB import populate
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from main.scraping import extraer_ropaHombre, indexar_datos
from main.search import buscar_ropa  
import os 
from whoosh.index import create_in, open_dir



def poblar_base_datos(request):
    try:
        extraer_ropaHombre()  
        messages.success(request, "La base de datos ha sido poblada correctamente.")
    except Exception as e:
        messages.error(request, f"Ocurrió un error: {e}")
    return redirect('pagina_inicio')

def indexar_datos(request):
    index_dir = "Index"
    
    # Verificar si el índice ya existe
    if os.path.exists(index_dir):
        # Si el índice ya existe, mostrar un mensaje de confirmación
        messages.warning(request, "El índice ya existe. ¿Está seguro de que quiere recargar los datos? Esta operación puede ser lenta.")
        
        # Si el usuario confirma, podemos proceder a recargar los datos
        if request.method == "POST":
            # Aquí debes agregar la lógica para volver a indexar los datos
            # Por ejemplo, si ya existe, puedes eliminar los datos actuales y volver a indexar.
            ix = open_dir(index_dir)
            writer = ix.writer()
            # Aquí indexarías los nuevos datos
            writer.commit()
            
            messages.success(request, "Datos recargados correctamente.")
            return redirect('pagina_inicio')
        else:
            # Mostrar un formulario de confirmación en la plantilla
            return render(request, 'confirmar_recarga.html')

    else:
        # Si el índice no existe, crearlo y indexar los datos
        os.makedirs(index_dir)
        ix = create_in(index_dir, schema)  # Asegúrate de tener el esquema definido
        writer = ix.writer()
        # Aquí agregarías la lógica para indexar los datos
        writer.commit()
        
        messages.success(request, "Índice creado y datos indexados correctamente.")
        return redirect('pagina_inicio')

def pagina_inicio(request):
    return render(request, 'pagina_inicio.html')

def lista_ropa_hombre(request):
    ropa_hombre = RopaHombre.objects.all()

    return render(request, 'lista_ropa_hombre.html', {'ropa_hombre': ropa_hombre})


def buscar_ropa_hombre(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = buscar_ropa(query)
    return render(request, 'buscar.html', {'results': results, 'query': query})