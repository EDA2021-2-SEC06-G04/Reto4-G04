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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

#####-----#####-----#####-----#####-----#####   ####---#####---####   #####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####   IMPORTACIÓN MÓDULOS   #####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####   ####---#####---####   #####-----#####-----#####-----#####-----#####

import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config




#####-----#####-----#####-----#####-----#####   ########-----######-----########   #####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####   DEFINICIÓN ESTRUCTURAS ELEMENTOS   #####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####   ########-----######-----########   #####-----#####-----#####-----#####-----#####

"""
    Se define la estructura que contiene el analizador.

"""

def new_analyzer ():
    """ 
        Esta funución permite inicializar el analizador. Este cuenta con las siguientes estructuras:
         1- city-id (mapa).
         2- id-city_info (mapa).

        dirigido: grafo dirigido con vértices en cada aereopuerto y arcos para
        cada vuelo que los relaciona en la dirección correspondiente.
        no_dirigido: Grafo para representar las relaciones entre aereopuertos de 
        forma que dos aereopuertos se relacionan solo si hay un vuelo directo de ida y otro de vuelta entre ambos.

        ciudades: índice que tiene por llave el nombre de una ciudad y por valor una lista de todas las ciudades diferentes con el nombre.

    """
    try:
        
        # Definir variable que guarda la información del analizar e inicializarla.
        analyzer = {}


        #####-----#####-----#####   Definición Grafos   #####-----#####-----#####

        """
            A continuación se crearán grafos por diferentes criterios.
            Es importante notar que todos los maps referencian a la misma información.
        
        """
        
        analyzer['dirigido'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=5000,comparefunction=comparerutas)
        

        analyzer['bigrafo'] = gr.newGraph(datastructure = 'ADJ_LIST',
                                      directed = True,
                                      size = 9076,
                                      comparefunction = compareStopIds)


        #####-----#####-----#####   Definición Listas   #####-----#####-----#####

        """
            A continuación se crearán listas por diferentes criterios.
            Es importante notar que todos los maps referencian a la misma información.
        
        """

        # Lista que guarda la información de todas las ciudades.
        analyzer['lt_cities'] = lt.newList('ARRAY_LIST')


        #####-----#####-----#####   Definición Maps/Índices   #####-----#####-----#####

        """
            A continuación se crearán maps por diferentes criterios
            para llegar a la información requerida en el menor tiempo posible.

            Es importante notar que todos los maps referencian a la misma información.
        
        """

        analyzer['NameAereopuertos'] = mp.newMap(maptype='PROBING', numelements=10000)

        analyzer['IATA'] = mp.newMap(maptype='PROBING', numelements=10000)

        analyzer['ciudades'] = mp.newMap(maptype='PROBING', numelements=9000)

        analyzer['routes'] = mp.newMap(numelements=9076,
                                  maptype = 'PROBING')

        # Mapa no ordenado cuyas llaves son nombres de ciudades y cuyas llaves son listas enlazadas que contienen
        # los id de las ciudades identificadas con ese nombre.
        analyzer['city-id'] = mp.newMap(numelements = 41002, maptype = "PROBING")

        # Mapa no ordenado cuyas llaves son id de ciudades y cuyas llaves son diccionarios de Python que guardan la 
        # información de interés de la ciudad identificada con dicho id.
        analyzer['id-city_info'] = mp.newMap(numelements = 41002, maptype = "PROBING")


        # Retornar el analizador.
        return analyzer

    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')




#####-----#####-----#####-----#####-----#####   ###---###----###   #####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####   ADICIÓN DE DATOS   #####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####   ###---###----###   #####-----#####-----######-----####-----#####

"""
    Se definen las funciones que permitirán añadir elementos al las
    estrucutras del analizador.

"""

def add_airport (analyzer: dict, airport: dict) -> dict:
    """
        Agrega un aereopuerto a las estrucutras del analizador.

        Parámetros:
            -> analyzer (dict): analizador.
            -> airport (dict): diccionario que representa un aeropuerto.

        Retorno:
            -> (dict): el analizador.

    """
    mp.put(analyzer['IATA'],airport['IATA'],airport)
    mp.put(analyzer['NameAereopuertos'],airport['Name'],airport)    
    gr.insertVertex(analyzer['dirigido'],airport['IATA'])
    if not mp.contains(analyzer['ciudades'],airport['City']):
        mp.put(analyzer['ciudades'],airport['City'],lt.newList(datastructure='ARRAY_LIST'))
    lt.addLast(me.getValue(mp.get(analyzer['ciudades'],airport['City'])),airport)
    return analyzer



def mp_add_route (analyzer: dict, departure: str, destination:str, distance: float) -> None:
    
    mp_routes = analyzer['routes']
    exists = mp.contains(mp_routes, departure)

    if exists:

        mp_destinatios = mp.get(mp_routes, departure)['value']
        mp.put(mp_destinatios, destination, distance)

    else:
        new_mp_destinatios = mp.newMap(maptype = 'PROBING')
        mp.put(new_mp_destinatios, destination, distance)
        mp.put(mp_routes, departure, new_mp_destinatios)



def no_dir_add_airport (analyzer: dict, airport_id: str) -> None:
    if not (gr.containsVertex(analyzer['bigrafo'], airport_id)):
        gr.insertVertex(analyzer['bigrafo'], airport_id)



def add_route (analyzer: dict, origin: str, destination: str, distance: float) -> None:
    edge = gr.getEdge(analyzer['bigrafo'], origin, destination)
    if (edge == None):
        gr.addEdge(analyzer['bigrafo'], origin, destination, distance)
     


def addruta(catalog,ruta):
    """
        Agrega una ruta aérea a los grafos.

    """
    
    #vertices = gr.vertices(catalog['dirigido'])
    
    gr.addEdge(catalog['dirigido'],ruta['Departure'],ruta['Destination'],ruta['distance_km'])
    return catalog



def add_id (analyzer: dict, param_city: str, id: int) -> None:
    """
        Esta función permite agregar una pareja llave-valor al map 'city-id' del catálogo.
        
        La llave deberá ser una ciudad, es decir, una cadena de caracteres.
        El valor será una lista enlazada cuyos elementos son ids (es decir, números enteros) con los cuales
        dicha ciudad se identifica.

        Parámetros:
            -> analyzer (dict): analizador.
            -> param_city (str): ciudad.
            -> id (int): id con el que la ciudad se identifica.

        No tiene retorno.
    
    """

    mp_city = analyzer ['city-id']               # Guardar el mapa 'city-id'.
    exists = mp.contains(mp_city, param_city)    # Determinar si la pareja llave-valor ya existe.

    # Si ya existe la pareja llave-valor.
    if (exists):

        # Crear variable que guarda la lista de los ids.
        lt_ids = mp.get(mp_city, param_city)['value']
        lt.addLast(lt_ids, id)


    # Si no existe la pareja llave-valor.
    else:

        # Crear una nueva lista de ids, añadir el id a dicha y añadir la pareja al map.
        new_lt_ids = lt.newList('ARRAY_LIST')
        lt.addLast(new_lt_ids, id)
        mp.put(mp_city, param_city, new_lt_ids)



def add_city_info (analyzer: dict, param_id: int, city_info: dict) -> None:
    """
        Esta función permite agregar una pareja llave-valor al map 'id-city_info' del catálogo.
        
        La llave deberá ser un id, es decir, un número entero.
        El valor será un diccionario de Python que guarda toda la información de la ciudad identificada
        con dicho id. 

        Parámetros:
            -> analyzer (dict): analizador.
            -> param_id (int): id de la ciudad.
            -> city_info (dict): diccionario con la info. de la ciudad.

        No tiene retorno.
    
    """

    # Guardar el mapa 'id-city_info' y añadir pareja llave-valor.
    mp_id = analyzer ['id-city_info']
    mp.put(mp_id, param_id, city_info)



def lt_add_city (analyzer: dict, city_info: dict) -> None:
    """
        Esta función permite agregar una ciudad a la lista 'lt_cities' del catálogo.

        Parámetros:
            -> analyzer (dict): analizador.
            -> city_info (dict): diccionario con la info. de la ciudad.

        No tiene retorno.
    
    """

    # Guardar lista y añadir la ciudad a dicha.
    lt_cities = analyzer['lt_cities']
    lt.addLast(lt_cities, city_info)


#####-----#####-----#####-----#####-----#####   ###---####----###   #####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####   CREACIÓN DE DATOS   #####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####   ###---####----###   #####-----#####-----######-----####-----#####

"""
    Se define las funciones que permitirán crear elementos referentes a información
    de interés del catálogo.

"""

def new_city (city_info: dict) -> dict:
    """
        Esta función permite crear un diccionario que almacenará la información de interés de una ciudad.
        Estos se representarán mediante el tipo de dato dict de Python.

        Parámetros:
            -> city_info (dict): diccionario que tiene toda la información de interés de la ciudad.

        Retorno:
            -> (dict): diccionario que representa la ciudad.

    """

    # Crear variable que guardará el diccionario de la ciudad.
    city = {}

    # Añadir los datos de interés.
    city['city'] = city_info['city']
    city['city_ascii'] = city_info['city_ascii']
    city['lat'] = city_info['lat']
    city['lng'] = city_info['lng']
    city['country'] = city_info['country']
    city['iso2'] = city_info['iso2']
    city['iso3'] = city_info['iso3']
    city['admin_name'] = city_info['admin_name']
    city['capital'] = city_info['capital']
    city['population'] = city_info['population']
    city['id'] = city_info['id']

    # Cambiar datos desconocidos a 'N.A.'.
    for key in city:
        if (city[key] == ''):
            city[key] = 'N.A.'
    
    # Convertir latitud, longitud, poblaión e id en decimales y enteros.
    if not (city['lat'] == 'N.A.'):
        city['lat'] = float(city['lat'])
    if not (city['lng'] == 'N.A.'):
        city['lng'] = float(city['lng'])
    if not (city['population'] == 'N.A.'):
        city['population'] = int(float(city['population']))
    if not (city['id'] == 'N.A.'):
        city['id'] = int(float(city['id']))

    # Retornar la ciuad.
    return city




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
    return gr.numEdges(analyzer['dirigido'])


def total_airports (analyzer: dict) -> int:
    """
        Esta función retorna el total de aereopuertos (vértices) del grafo.

        Parámetros:
            -> analyzer (dict): analizador.

        Retorno:
            -> (int): total de rutas de aeropuertos.

    """ 
    return gr.numVertices(analyzer['dirigido'])


def no_dir_total_routes (analyzer: dict) -> int:
    """
        Esta función retorna el total de rutas de vuelo (arcos) del grafo.

        Parámetros:
            -> analyzer (dict): analizador.

        Retorno:
            -> (int): total de rutas de vuelo.

    """
    return gr.numEdges(analyzer['bigrafo'])


def nor_dir_total_airports (analyzer: dict) -> int:
    """
        Esta función retorna el total de aereopuertos (vértices) del grafo.

        Parámetros:
            -> analyzer (dict): analizador.

        Retorno:
            -> (int): total de rutas de aeropuertos.

    """
    return gr.numVertices(analyzer['bigrafo'])




#####-----#####-----#####-----#####-----#####   #####---#######----#####   #####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####   FUNCIONES DE COMPARACIÓN   #####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####   #####---#######----#####   #####-----#####-----#####-----#####-----#####

"""
    A continuación se definen las funciones que permitirán comparar
    y ordenar los elementos del catálogo (incluyendo las llaves de los mapas).

"""

def comparerutas(stop, keyvaluestop):
    """
        Compara dos estaciones.

    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1



def compareStopIds(stop, keyvaluestop):
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1



# Esta función compara los id de una ciudad.
def cmp_cities (city:dict, id: int) -> int:
    """
    """
    
    # Guardar el id de la ciudad y crear variable retorno.
    id_city = city['id']
    ans = -1

    # Comparar los id y retornar.
    if (id_city == id):
        ans = 0
    elif (id_city < id):
        ans = 1
    return ans