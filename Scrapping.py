#encoding:utf-8

from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import messagebox
import sqlite3
import re


# lineas para evitar error SSL
import os, ssl
from lxml.html._diffcommand import description
from whoosh.automata.fsa import find_all_matches
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context


def extraer_productos():
    lista=[]
    
    url="https://pbsapparel.com/collections/ropa"
    f = urllib.request.urlopen(url)
    s = BeautifulSoup(f,"lxml")      
    
    productos = s.find_all("div", class_="product-grid-item__info") 
    for producto in productos:

        nombre = producto.find("a", class_="product-grid-item__title").get_text(strip=True)
        enlace = "https://pbsapparel.com" + producto.find("a", class_="product-grid-item__title")["href"]
    

        f1 = urllib.request.urlopen(enlace)
        j = BeautifulSoup(f1, "lxml")
        
        precio = j.find("span", class_="product__price--regular").get_text(strip=True)
        
        precioOriginal = j.find("s", class_="product__price--compare").get_text(strip=True)
        
        if (j.find("span", class_="descuento-flag") is not None):
            descuento = j.find("span", class_="descuento-flag").get_text(strip=True)

        tallas = j.find("div", class_="product__selectors 24").find_all("span")
        listaTallas = []
        for talla in tallas:
            letra = talla.get_text().replace("\n", "")
            if (letra not in listaTallas):
                listaTallas.append(letra)
        listaTallas = str(listaTallas[1:]).replace("'", "")

        """
        detalles = str(j.find("div", class_="product__block product__accordions").find("p").find("span"))
        detalles = detalles.replace('<span class="metafield-multi_line_text_field">', "").replace("</span>", "").split("<br/>")
        detallesAdicionales = []
        for linea in detalles :
            detallesAdicionales.append(linea)
        """
        
        lista.append((nombre, enlace, precio, precioOriginal, descuento, listaTallas))
        
    return lista

def almacenar_bd():
    conn = sqlite3.connect('productos.db')
    conn.text_factory = str
    conn.execute("DROP TABLE IF EXISTS PRODUCTOS") 
    conn.execute('''CREATE TABLE PRODUCTOS
       (NOMBRE        TEXT    NOT NULL,
       LINK          TEXT   NOT NULL,
       PRECIO        TEXT    NOT NULL,
       PRECIOORIGINAL   TEXT    NOT NULL,
       DESCUENTO    TEXT    NOT NULL,
       TALLAS   TEXT    NOT NULL);''')

    for i in extraer_productos():              
        conn.execute("""INSERT INTO PRODUCTOS VALUES (?,?,?,?,?,?)""",i)
    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM PRODUCTOS")
    messagebox.showinfo( "Base Datos", "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    conn.close()

def imprimir_lista(cursor):
    v = Toplevel()
    v.title("ROPA DE HOMBRE:")
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width = 150, yscrollcommand=sc.set)
    for row in cursor:
        lb.insert(END,row[0])
        lb.insert(END,"    Precio: "+ row[2])
        if (row[3] != ""):  
            lb.insert(END,"    Precio original: "+ row[3])
        if (row[3] != ""):  
            lb.insert(END, "    Descuento: " + row[4])
        lb.insert(END, "    Más detalles: " + row[1])
        lb.insert(END,"    Tallas: "+ row[5])
        lb.insert(END,"\n\n")
    lb.pack(side=LEFT,fill=BOTH)
    sc.config(command = lb.yview)

def listar_productos():
    conn = sqlite3.connect('productos.db')
    conn.text_factory = str  
    cursor = conn.execute("SELECT * FROM PRODUCTOS")
    imprimir_lista(cursor)
    conn.close()
  


def ventana_principal():       
    root = Tk()
    root.geometry("150x100")

    menubar = Menu(root)
    

    datosmenu = Menu(menubar, tearoff=0)
    datosmenu.add_command(label="Cargar", command=almacenar_bd)
    datosmenu.add_separator()   
    datosmenu.add_command(label="Salir", command=root.quit)
    
    buscarmenu = Menu(menubar, tearoff=0)
    buscarmenu.add_command(label="Productos", command=listar_productos)

    menubar.add_cascade(label="Datos", menu=datosmenu)
    menubar.add_cascade(label="Listar", menu=buscarmenu)
    
    
        
    root.config(menu=menubar)
    root.mainloop()

    

if __name__ == "__main__":
    ventana_principal()