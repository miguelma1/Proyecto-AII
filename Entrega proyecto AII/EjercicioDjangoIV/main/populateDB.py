import requests
from bs4 import BeautifulSoup
from main.models import RopaHombre
from whoosh.index import create_in


def extraer_ropaHombre():

    RopaHombre.objects.all().delete()
    
    lista = []
    url = "https://pbsapparel.com/collections/ropa"
    f = requests.get(url)
    s = BeautifulSoup(f.content, "lxml")

    ropasHombre = s.find_all("div", class_="product-grid-item__info")
    for ropaHombre in ropasHombre:
        nombre = ropaHombre.find("a", class_="product-grid-item__title").get_text(strip=True)
        enlace = "https://pbsapparel.com" + ropaHombre.find("a", class_="product-grid-item__title")["href"]
        
        f1 = requests.get(enlace)
        j = BeautifulSoup(f1.content, "lxml")
        
        precio = j.find("span", class_="product__price--regular").get_text(strip=True)
        precio_original = j.find("s", class_="product__price--compare")
        precio_original = precio_original.get_text(strip=True) if precio_original else ""
        
        descuento = j.find("span", class_="descuento-flag")
        descuento = descuento.get_text(strip=True) if descuento else ""
        
        tallas = j.find("div", class_="product__selectors 24").find_all("span")
        lista_tallas = [talla.get_text().replace("\n", "") for talla in tallas]
        lista_tallas = str(lista_tallas[1:]).replace("'", "")
        
        ropaHombre_db = RopaHombre(
            nombre=nombre,
            enlace=enlace,
            precio=precio,
            precio_original=precio_original,
            descuento=descuento,
            tallas=lista_tallas
        )
        ropaHombre_db.save()

    print("Ropa de hombre guardada en la base de datos.")

def indexar_datos():
    schem = Schema(nombre=TEXT(stored=True), enlace=TEXT(stored=True), precio=TEXT(stored=True), precio_original=TEXT(stored=True), descuento=TEXT(stored=True), tallas=TEXT(stored=True))
    
    if os.path.exists("Index"):
        shutil.rmtree("Index")
    os.mkdir("Index")
    
    ix = create_in("Index", schema=schem)
    writer = ix.writer()
    i=0
    lista=extraer_ropaHombre()()
    for j in lista:
        writer.add_document(nombre=str(j[0]), enlace=int(j[1]), precio=str(j[2]), precio_original=j[3], descuento=str(j[4]), tallas=str(j[5]))    
        i+=1
    writer.commit()
    messagebox.showinfo("Fin de indexado", "Se han indexado "+str(i)+ " prendas de ropa de hombre") 