"""
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

#####-----#####-----#####-----#####-----#####-----#####   ####---#####---####   #####-----#####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####-----#####   IMPORTACIÓN MÓDULOS   #####-----#####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####-----#####   ####---#####---####   #####-----#####-----#####-----#####-----#####-----#####

import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT.graph import gr
from DISClib.ADT import map as mp
import model
import csv




#####-----#####-----#####-----#####-----#####   ##########-----###########-----##########   #####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####   FUNCIONES INICIALIZACIÓN Y CARGA DE DATOS   #####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####   ##########-----###########-----##########   #####-----#####-----#####-----#####-----#####

"""
    Se definen las funciones que permitirán inicializar el analizador y cargar
    los elementos de la base de datos.

"""

# Inicialización del Catálogo
def init() -> dict:
    """
        Llama la funcion de inicializacion  del modelo.

    """
    # catalog es utilizado para interactuar con el modelo
    catalog = model.newcatalog()
    return catalog



# Función que carga toda la información al analizador.
def load_data (analyzer: dict) -> None:
    """
        Esta función carga toda la información al analizador.

        Parámetro:
            -> analyzer (dict): analizador.

        No tiene retorno.

    """

    # Crear variables que guardan la referencia al archivo de las ciudades y toda
    # su información.
    file = cf.data_dir + '\\Skylines\\worldcities.csv'
    input_file = csv.DictReader(open(file, encoding='utf-8'))

    # Iterar sobre cada ciudad de la base de datos.
    for city_info in input_file:

        city = model.new_city(city_info)    # Crear diccionario con la información de la ciudad.
        name = city['city']                 # Guardar su nombre.
        id = city['id']                     # Guardar su id.

        model.add_id(analyzer, name, id)            # Añadirla al mapa 'city-id'.
        model.add_city_info(analyzer, id, city)     # Añadirla al mapa 'id-city_info'.
        


# Funciones para la carga de datos
def loadciudades(catalog):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un vértice por cada aereopuerto en el archivo
    """
    ciudadesfile = cf.data_dir + '\\Skylines\\worldcities.csv'
    input_file = csv.DictReader(open(ciudadesfile, encoding="utf-8"),
                                delimiter=",")
                                
    for ciudad in input_file:
        model.addciudad(catalog, ciudad)
    return catalog

def loadaereopuertos(catalog):
    """
        Carga los datos de los archivos CSV en el modelo.
        Se crea un vértice por cada aereopuerto en el archivo.

    """
    aereopuertosfile = cf.data_dir + '\\Skylines\\airports_full.csv'
    input_file = csv.DictReader(open(aereopuertosfile, encoding="utf-8"),
                                delimiter=",")
    f = None
    for aereopuerto in input_file:
        if f == None:
            f = aereopuerto
        model.addaereopuerto(catalog, aereopuerto)
    return catalog,f



def loadrutas(catalog):
    """
        Carga los datos de los archivos CSV en el modelo.
        Se crea un arco entre cada par de aereopuertos que
        tienen una ruta en un sentido.

    """
    rutasfile = cf.data_dir + '\\Skylines\\routes_full.csv'
    input_file = csv.DictReader(open(rutasfile, encoding="utf-8"),
                                delimiter=",")
    for ruta in input_file:
        model.addruta(catalog, ruta)
    return catalog



def load_routes (analyzer: dict) -> None:

    file = cf.data_dir + '\\Skylines\\routes_full.csv'
    input_file = csv.DictReader(open(file, encoding='utf-8'))

    for route in input_file:
        
        departure = route['Departure']
        destination = route['Destination']
        distance = float(route['distance_km'])

        model.mp_add_route(analyzer, departure, destination, distance)

    mp_routes = analyzer['routes']
    
    for destination in (lt.iterator(mp.keySet(mp_routes))):
        mp_departures = mp.get(mp_routes, destination)['value']
        for departure in (lt.iterator(mp.keySet(mp_departures))):
            if (mp.contains(mp_routes, departure)):
                mp_departure_departures = mp.get(mp_routes, departure)['value']
                if mp.contains(mp_departure_departures, destination):
                    model.add_airport(analyzer, departure)
                    model.add_airport(analyzer, destination)
                    model.add_route(analyzer, departure, destination, distance)




#####-----#####-----#####-----#####-----#####   ####---######----####   #####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####   FUNCIONES DE CONSULTA   #####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####   ####---######----####   #####-----#####-----######-----####-----#####

"""
    Se define las funciones que permitirán acceder a información de interés de
    las estructuras.

"""

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

def totalrutasnodir(catalog):
    """
    Total de vuelos entre aereopuertos
    """
    return model.totalrutasnodir(catalog)

def totalaereopuertosnodir(catalog):
    """
    Total de aereopuertos en el grafo
    """
    return model.totalaereopuertosnodir(catalog)