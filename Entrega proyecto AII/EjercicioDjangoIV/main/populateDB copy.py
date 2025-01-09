#encoding:utf-8
from main.models import Vino, Denominacion, Uva, Pais

path = "data"

def populatePais():
    Pais.objects.all().delete()
    
    lista=[]
    fileobj=open(path+"\\paises", "r")
    for line in fileobj.readlines():
        rip = str(line.strip()).split('|')
        lista.append(Pais(idPais=int(rip[0].strip()), nombre=str(rip[1].strip())))
    fileobj.close()
    Pais.objects.bulk_create(lista)  # bulk_create hace la carga masiva para acelerar el proceso
    
    return len(lista)

def populateDenominacion():
    Denominacion.objects.all().delete()
    
    lista=[]
    fileobj=open(path+"\\denominaciones", "r")
    for line in fileobj.readlines():
        rip = str(line.strip()).split('|')
        lista.append(Denominacion(idDenominacion=int(rip[0].strip()), nombre=str(rip[1].strip()), pais=Pais.objects.get(idPais=int(rip[2].strip()))))
    fileobj.close()
    Denominacion.objects.bulk_create(lista)  # bulk_create hace la carga masiva para acelerar el proceso
    
    return len(lista)

def populateUva():
    Uva.objects.all().delete()
    
    lista=[]
    fileobj=open(path+"\\uvas", "r")
    for line in fileobj.readlines():
        rip = str(line.strip()).split('|')
        lista.append(Uva(idUva=int(rip[0].strip()), nombre=str(rip[1].strip())))
    fileobj.close()
    Uva.objects.bulk_create(lista)  # bulk_create hace la carga masiva para acelerar el proceso
    
    return len(lista)

def populateVino():
    Vino.objects.all().delete()
    
    fileobj=open(path+"\\vinos", "r")
    for line in fileobj.readlines():
        rip = line.strip().split('|')
      
        vi = Vino(idVino=int(rip[0].strip()), nombre=str(rip[1].strip()), precio=float(rip[2].strip()), denominacion=Denominacion.objects.get(idDenominacion=int(rip[3].strip())))
        vi.save()
        
        lista_aux=[]
        for i in range(4, len(rip)):
            lista_aux.append(Uva.objects.get(idUva = int(rip[i].strip())))
    
        vi.uvas.set(lista_aux)
        
    fileobj.close()    


    return Vino.objects.count()


def populate():
    p = populatePais()
    d = populateDenominacion()
    u = populateUva()
    v = populateVino()
    return (p,d,u,v)