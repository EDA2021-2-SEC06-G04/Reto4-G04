﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import csv



"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo
def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    catalog = model.newcatalog()
    return catalog

# Funciones para la carga de datos
def loadaereopuertos(catalog, aereopuertosfile):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un vértice por cada aereopuerto en el archivo
    """
    aereopuertosfile = cf.data_dir + aereopuertosfile
    input_file = csv.DictReader(open(aereopuertosfile, encoding="utf-8"),
                                delimiter=",")
    for aereopuerto in input_file:
        model.addaereopuerto(catalog, aereopuerto)
    return catalog

def loadrutas(catalog, rutasfile):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de aereopuertos que
    tienen una ruta en un sentido.
    """
    rutasfile = cf.data_dir + rutasfile
    input_file = csv.DictReader(open(rutasfile, encoding="utf-8"),
                                delimiter=",")
    for ruta in input_file:
        model.addruta(catalog, ruta)
    return catalog

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def totalrutas(catalog):
    """
    Total de vuelos entre aereopuertos
    """
    return model.totalrutas(catalog)

def totalaereopuertos(catalog):
    """
    Total de aereopuertos en el grafo
    """
    return model.totalaereopuertos(catalog)
