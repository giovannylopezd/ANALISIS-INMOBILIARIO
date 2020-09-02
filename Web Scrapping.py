import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


urlbase = 'https://www.infocasas.com.bo/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}

link_casas = []

for x in range(1,31):
  r = requests.get(f'https://www.infocasas.com.bo/venta/casas-y-departamentos-y-condominio/santa-cruz/pagina{x}?&ordenListado=5', headers=headers)
  soup = BeautifulSoup(r.content, 'html.parser')
  lista_casas = soup.find_all('div', class_= 'propiedades-slider ')
  for item in lista_casas:
    for link in item.find_all('a', href=True):
      link_casas.append(urlbase + link['href'])

link_casas = set(link_casas)
print(len(link_casas))            

#testlink = 'https://www.infocasas.com.bo/venta-departamento-con-financiamiento-directo-al-100/186526102?v'


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
        'precio': precio,
        'zona': zona
        }
    
    lista_items.append(casas)
    print('Guardando: Inmueble', len(lista_items),'zona ',casas['zona'])
    

df = pd.DataFrame(lista_items)
print(df.head(15))

df.to_csv('casas.csv', index = False)

