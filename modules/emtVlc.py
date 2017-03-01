#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
# https://docs.python.org/3.6/library/urllib.html 
import urllib.request  # for parsing URLs
import urllib.parse    # for opening and reading URLs
from bs4 import BeautifulSoup as bs

def get_parada(numParada,linea='',adaptados=0,user='Anonimo',idioma='es'):
    emtVars={'parada': numParada,
             'linea': linea,
             'adaptados': adaptados,
             'usuario': user,
             'idioma': idioma
             }
    emtVars = urllib.parse.urlencode(emtVars)
    emtArgs = emtVars.encode('ascii')
    emtUrl = 'https://www.emtvalencia.es/ciudadano/modules/mod_tiempo/busca_parada.php'
    req = urllib.request.Request(emtUrl, emtArgs)
    req.add_header("Content-type", "application/x-www-form-urlencoded")
    data = urllib.request.urlopen(req).read().decode('utf-8')
    return(data)



## Funciones temporales debugging
def emt_html(numParada):
    # Datos que provienen de la funcion get_parada
    raw_data = get_parada(numParada)
    soup = bs(raw_data, "html.parser")
    return(soup.prettify())

def soup_html(numParada):
    # Datos que provienen de la funcion get_parada
    raw_data = get_parada(numParada)
    soup = bs(raw_data, "html.parser")
    return(soup)

def prime_buses(numParada):
    # Objeto que proviene de la funcion soup_html
    data = soup_html(numParada)
    # Todos los span
    spans = data.select('span')
    # Los span con la imagen de la linea
    span_linea = data.find_all('span', {'class': 'imagenParada'})
    # Los span con el nombre de la linea y el tiempo
    span_tiempos = data.find_all('span', {'class': 'llegadaHome'})
    # Los img donde aparece la linea
    imgElem = data.select('img')
    buses = ""

    # Bucle para mostrar linea y tiempo
    ## Pdte de revisar problemas de encoding
    ## Pdte de añadir que si sale "Temporalmente fuera de servicio automaticamente meta F5"
    for span, img in zip(span_tiempos, imgElem):
        linea = img.get('title')
        show = span.getText(strip=True)
        show = show.encode('utf-8')
        show = str(show)
        show = show.replace("b'",": ")
        #print(linea, show)
        buses += linea+show+"\n"
    return buses
