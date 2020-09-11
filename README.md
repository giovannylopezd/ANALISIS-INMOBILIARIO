# Análisis_Inmobiliario

Proyecto sobre Extracción de Datos Inmobiliarios, limpieza, análisis y creación de modelo para proyección en Santa Cruz de la Sierra-Bolivia.

## Web_Scrapping
En esta ocasión, se utilizó el paquete **BeautifulSoup** de Python para poder extraer datos de una página de venta de inmuebles.  

## Limpieza de Datos
En cuanto la manipulación y limpieza, se utilizó únicamente el paquete **Tidyverse** en R y se logró dar formato a los datos en Precios, quitar valores atípicos entre precio y superficie construida en m2, también se limpiaron los nombres de las zonas dejando 6 zonas que abarcan la totalidad de la Ciudad.

## Predicción de Precios Inmobiliarios
Por la poca cantidad de datos se ha optado por modelos tradicionales, por lo que se han implementado:  
1. Regresión Lineal Múltiple.  
2. Regresión Polinómica.  
3. Regresión de Bosques Aleatorios.  

Este último fue el que se adaptó mejor a los datos de entrenamiento e hizo una mejor predicción, además de tener menores puntuaciones en las métricas de error **MAE** y **RMSE**.  
Una razón puede deberse a que Random Forest es bastante robusto a la hora de analizar conjuntos de datos categóricos y numéricos combinados dadas las decisiones que aportan cada uno de los árboles implementados, además de ser poco sensible a los atípicos y dispersión de variables.

