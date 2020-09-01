#!/usr/bin/env python
# coding: utf-8

# ##  Web Scrapping de Datos Inmobiliarios
# 
# Realizado por: **Giovanny Lopez**

# En este apartado realizaremos la extraccion de datos inmobiliarios en la ciudad de Santa Cruz de la Sierra.  
# La página que tomaremos, debido a su relevancia en la región, será [**Infocasas**](www.infocasas.com)

# In[1]:


import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


# 1. Creamos la variable con el **URL** principal de la página que deseamos analizar.  
# 2. Creamos un agente que imitará el ingreso de un humano a la página para poder acceder.  
# 3. Creamos una lista vacía para llenarla de los links que dirigen a cada anuncio de venta de inmuebles

# In[2]:


urlbase = 'https://www.infocasas.com.bo/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}

link_casas = []


# ### Anuncios de Venta de Inmuebles
# En este apartado necesitamos recabar la siguiente información:  
# 1. Número de páginas que queremos buscar
# 2. **URL** de la segunda página para obtener un indicador de página
# 3. Elemento de bloque donde se enlista la información de cada anuncio **('div','span',etc.)**,la clase y  
# verificar que contenga el elemento **'a'** con su respectivo enlace al anuncio en cada inmueble.  
# 
# Por último, al link obtenido en el **Paso 2** le añadimos una **f** (fstring) y reemplazamos el numero de página por **{x}**.  
# *Es así que conseguimos los links de cada anuncio, los adicionamos a la lista e iteramos la operación para cada página*

# In[3]:


pag = 30
for x in range(1,pag+1):
  r = requests.get(f'https://www.infocasas.com.bo/venta/casas-y-departamentos-y-condominio/santa-cruz/pagina{x}?&ordenListado=5', headers=headers)
  soup = BeautifulSoup(r.content, 'html.parser')
  lista_casas = soup.find_all('div', class_= 'propiedades-slider ')
  for item in lista_casas:
    for link in item.find_all('a', href=True):
      link_casas.append(urlbase + link['href'])

link_casas = set(link_casas) # Para eliminar los duplicados
print(len(link_casas))


# ### Datos de interés
# Para esto necesitamos ingresar a uno de los anuncios y recabar la información que más nos interese y que pueda estar en la mayoría de los anuncios.  
# 
# Los pasos son los siguientes:  
# 1. Inspeccionamos los datos de interés y ubicamos el elemento de bloque que los contiene junto a la clase
# 2. Damos un formato al texto obtenido según nuestra conveniencia
# 3. Ingresamos un **try** y un **except** para poder manejar el blucle en caso de error por falta de datos.
# 4. Creamos un diccionario que contenga todas las variables que hemos especificado en el bucle.
# 5. Agregamos datos de cada inmueble por cada iteración de nuestro bucle en nuestra lista creada al principio

# In[4]:


lista_items = []
for link in link_casas:
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.content,'lxml')
    
    try:
        tipo = soup.find('div', class_='dot home').text.strip()
        tipo = tipo.replace('Tipo de propiedad\n\n','')
    except:
        tipo = 'NA'
    
    try:
        dormitorios = soup.find('div', class_='dot bed').text.strip()
        dormitorios = re.sub("[^0-9]", "", dormitorios)
    except:
        dormitorios = 'NA'
    try:
        baños = soup.find('div', class_='dot shower').text.strip()
        baños = re.sub("[^0-9]", "", baños)
    except:
        baños = 'NA'
    
    try:
        garajes = soup.find('div', class_='dot cab').text.strip()
        garajes = re.sub("[^0-9]", "", garajes)
    except:
        garajes = str(0)
    
    try:
        m2 = soup.find('div', class_='dot m2').text.strip()
        m2 = re.sub("[^0-9]", "", m2)
    except:
        m2 = 'NA'
    
    try:
        precio = soup.find('p', class_='precio-final').text.strip()
        precio = precio.replace('U$S ','')
    except:
        precio = 'NA'
    
    try:
        titulo = soup.find('h1', class_='likeh2 titulo one-line-txt').text.strip()
    except:
        titulo = 'NA'
    
    try:
        zona = soup.find('p', class_='zona-nombre').text.strip()    
    except:
        zona = 'NA'
    
    casas = {
        'titulo': titulo,
        'tipo': tipo,
        'dormitorios': dormitorios,
        'baños': baños,
        'garajes': garajes,
        'm2': m2,
        'zona': zona,
        'precio': precio
        }
    
    lista_items.append(casas)
    print('Guardando: Inmueble', len(lista_items),'zona ',casas['zona'])


# ### Formato y Exportación
# Por último, daremos formato a nuestro datos y los exportaremos para manipularlos en otra ocasión

# In[5]:


df = pd.DataFrame(lista_items)
print(df.head(10))
df.to_csv('infocasas.csv', index = False)

