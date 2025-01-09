# scraping.py
import requests
from bs4 import BeautifulSoup
from main.models import Producto  # Importa tu modelo de Django

def extraer_productos():
    lista = []
    url = "https://pbsapparel.com/collections/ropa"
    f = requests.get(url)
    s = BeautifulSoup(f.content, "lxml")

    productos = s.find_all("div", class_="product-grid-item__info")
    for producto in productos:
        nombre = producto.find("a", class_="product-grid-item__title").get_text(strip=True)
        enlace = "https://pbsapparel.com" + producto.find("a", class_="product-grid-item__title")["href"]
        
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
        
        # Crear el objeto Producto y guardarlo en la base de datos
        producto_db = Producto(
            nombre=nombre,
            enlace=enlace,
            precio=precio,
            precio_original=precio_original,
            descuento=descuento,
            tallas=lista_tallas
        )
        producto_db.save()

    print("Productos guardados en la base de datos.")
