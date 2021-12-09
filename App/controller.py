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

def init () -> dict:
    """
        Llama la funcion de inicialización del analizador.

        No tiene parámetros.

        Retorno:
            -> (dict): el analizador.

    """
    analyzer = model.new_analyzer()
    return analyzer



def load_data (analyzer: dict) -> None:
    """
        Esta función carga toda la información al analizador.

        Parámetro:
            -> analyzer (dict): analizador.

        No tiene retorno.

    """
    # Invocar funciones para carga de datos.
    loadrutas(analyzer)
    load_routes(analyzer)
    load_cities(analyzer)
    loadaereopuertos(analyzer)



def load_cities (analyzer: dict) -> None:
    """
        Esta función carga la información de las ciudades al analizador.

        Parámetro:
            -> analyzer (dict): analizador.

        No tiene retorno.

    """

    # Crear variables que guardan la referencia al archivo de las ciudades y toda
    # su información.
    file = cf.data_dir + '\\Skylines\\worldcities-utf8.csv'
    input_file = csv.DictReader(open(file, encoding='utf-8'))

    # Iterar sobre cada ciudad de la base de datos.
    for city_info in input_file:

        city = model.new_city(city_info)    # Crear diccionario con la información de la ciudad.
        name = city['city']                 # Guardar su nombre.
        id = city['id']                     # Guardar su id.

        model.lt_add_city(analyzer, city)           # Añadirla a la lista 'lt_cities'.
        model.add_id(analyzer, name, id)            # Añadirla al mapa 'city-id'.
        model.add_city_info(analyzer, id, city)     # Añadirla al mapa 'id-city_info'.



def loadaereopuertos(analyzer: dict) -> tuple:
    """
        Carga los datos de los archivos CSV en el modelo.
        Se crea un vértice por cada aereopuerto en el archivo.

    """
    aereopuertosfile = cf.data_dir + '\\Skylines\\airports-utf8-small.csv'
    input_file = csv.DictReader(open(aereopuertosfile, encoding="utf-8"),
                                delimiter=",")
    z = None
    f = None
    for aereopuerto in input_file:
        if z == None:
            z = aereopuerto
        f = aereopuerto
        model.add_airport (analyzer, aereopuerto)
    return z,f



def loadrutas(analyzer: dict) -> dict:
    """
        Carga los datos de los archivos CSV en el modelo.
        Se crea un arco entre cada par de aereopuertos que
        tienen una ruta en un sentido.

    """
    rutasfile = cf.data_dir + '\\Skylines\\routes-utf8-small.csv'
    input_file = csv.DictReader(open(rutasfile, encoding="utf-8"),
                                delimiter=",")
    for ruta in input_file:
        model.addruta(analyzer, ruta)
    return analyzer



def load_routes (analyzer: dict) -> None:

    file = cf.data_dir + '\\Skylines\\routes-utf8-small.csv'
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
                    model.no_dir_add_airport(analyzer, departure)
                    model.no_dir_add_airport(analyzer, destination)
                    model.add_route(analyzer, departure, destination, distance)




#####-----#####-----#####-----#####-----#####   ####---######----####   #####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####   FUNCIONES DE CONSULTA   #####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####   ####---######----####   #####-----#####-----######-----####-----#####

"""
    Se define las funciones que permitirán acceder a información de interés de
    las estructuras.

"""

def total_routes (analyzer: dict) -> int:
    """
        Esta función retorna el total de rutas de vuelo (arcos) del grafo.

        Parámetros:
            -> analyzer (dict): analizador.

        Retorno:
            -> (int): total de rutas de vuelo.

    """
    return model.total_routes(analyzer)


def total_airports (analyzer: dict) -> int:
    """
        Esta función retorna el total de aereopuertos (vértices) del grafo.

        Parámetros:
            -> analyzer (dict): analizador.

        Retorno:
            -> (int): total de rutas de aeropuertos.

    """ 
    return model.total_airports(analyzer)


def no_dir_total_routes (analyzer: dict) -> int:
    """
        Esta función retorna el total de rutas de vuelo (arcos) del grafo.

        Parámetros:
            -> analyzer (dict): analizador.

        Retorno:
            -> (int): total de rutas de vuelo.

    """
    return model.no_dir_total_routes(analyzer)



def nor_dir_total_airports (analyzer: dict) -> int:
    """
        Esta función retorna el total de aereopuertos (vértices) del grafo.

        Parámetros:
            -> analyzer (dict): analizador.

        Retorno:
            -> (int): total de rutas de aeropuertos.

    """
    return model.nor_dir_total_airports(analyzer)

def interconnections(analyzer):
    """
    Devuelve una lista con los diccionarios de los aereopuertos más interconectados en la red
    """
    return model.interconnections(analyzer)

def closestAirport(analyzer,city):
    '''
    Devuelve el diccionario del aereopuerto más cercano por coordenadas a las coordenadas de la ciudad que llega
    como un diccionario por parámetro.
    '''
    return model.closestAirport(analyzer,city)

def shortestRoute(analyzer,first_airport,last_airport):
    '''
    Devuelve el camino más corto en kilómetros par air d eun aereopuerto a otro
    '''
    return model.shortestRoute(analyzer,first_airport,last_airport)