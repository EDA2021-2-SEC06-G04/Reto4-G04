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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

#####-----#####-----#####-----#####-----#####   ####---#####---####   #####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####   IMPORTACIÓN MÓDULOS   #####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####   ####---#####---####   #####-----#####-----#####-----#####-----#####

from math import inf
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from haversine import haversine
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
                                              size=300,comparefunction=comparerutas)
        

        analyzer['bigrafo'] = gr.newGraph(datastructure = 'ADJ_LIST',
                                      directed = False,
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

        analyzer['cities_airports'] = mp.newMap(maptype='PROBING', numelements=9000)

        analyzer['connections'] = mp.newMap(maptype='PROBING')

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
    mp.put(analyzer['IATA'], airport['IATA'], airport)
    mp.put(analyzer['NameAereopuertos'],airport['Name'],airport)    
    if not mp.contains(analyzer['cities_airports'],airport['City']):
        mp.put(analyzer['cities_airports'],airport['City'],lt.newList(datastructure='ARRAY_LIST'))
    lt.addLast(me.getValue(mp.get(analyzer['cities_airports'],airport['City'])),airport)
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
     


def addruta(analyzer,ruta):
    """
        Agrega una ruta aérea a los grafos y suma una conexión a cada aereopuerto
    """
    if not gr.containsVertex(analyzer['dirigido'],ruta['Departure']):
        gr.insertVertex(analyzer['dirigido'],ruta['Departure'])
    if not gr.containsVertex(analyzer['dirigido'],ruta['Destination']):
        gr.insertVertex(analyzer['dirigido'],ruta['Destination'])
    if gr.getEdge(analyzer['dirigido'],ruta['Departure'],ruta['Destination']) == None:
        gr.addEdge(analyzer['dirigido'],ruta['Departure'],ruta['Destination'],float(ruta['distance_km']))
    mp_connections = analyzer['connections']
    exists = mp.contains(mp_connections, ruta['Departure'])
    if exists:
        if mp.contains(mp.get(mp_connections,ruta['Departure'])['value'],'Departure'):
            mp.put(mp.get(mp_connections,ruta['Departure'])['value'], 'Departure', me.getValue(mp.get(mp.get(mp_connections,ruta['Departure'])['value'],'Departure')) + 1)
        else:
            mp.put(mp.get(mp_connections,ruta['Departure'])['value'], 'Departure', 1)
    else:
        mp.put(mp_connections, ruta['Departure'], mp.newMap())
        mp.put(mp.get(mp_connections, ruta['Departure'])['value'],'Departure', 1)
        mp.put(mp.get(mp_connections, ruta['Departure'])['value'],'Destination', 0)
    exists = mp.contains(mp_connections, ruta['Destination'])
    if exists:
        if mp.contains(mp.get(mp_connections,ruta['Destination'])['value'],'Destination'):
            mp.put(mp.get(mp_connections,ruta['Destination'])['value'], 'Destination', me.getValue(mp.get(mp.get(mp_connections,ruta['Destination'])['value'],'Destination')) + 1)
        else:
            mp.put(mp.get(mp_connections,ruta['Destination'])['value'], 'Destination', 1)
    else:
        mp.put(mp_connections, ruta['Destination'], mp.newMap())
        mp.put(mp.get(mp_connections, ruta['Destination'])['value'],'Destination', 1)
        mp.put(mp.get(mp_connections, ruta['Destination'])['value'],'Departure', 0)
    
    return analyzer




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

#Consultas en al carga de datos
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

#Requerimiento 1
def interconnections(analyzer):
    """
    Retorna una lista con los 5 aereopuetos más interconectados de la red (solo sus IATA)
    """
    airports = mp.keySet(analyzer['connections'])
    ordered = lt.newList(datastructure='ARRAY_LIST')
    for airport in lt.iterator(airports):
        if lt.size(ordered) == 0:
            lt.addLast(ordered,airport)
        elif lt.size(ordered) >= 5:
            i = 1
            while i <= 5:
                
                if mp.get(mp.get(analyzer['connections'],airport)['value'],'Departure')['value'] + mp.get(mp.get(analyzer['connections'],airport)['value'],'Destination')['value'] >= mp.get(mp.get(analyzer['connections'],lt.getElement(ordered,i))['value'],'Departure')['value'] + mp.get(mp.get(analyzer['connections'],lt.getElement(ordered,i))['value'],'Destination')['value']:
                    lt.insertElement(ordered,airport,i)
                    lt.removeLast(ordered)
                    break
                i += 1
        else:
            i = 1
            while i <= lt.size(ordered):
                
                if mp.get(mp.get(analyzer['connections'],airport)['value'],'Departure')['value'] + mp.get(mp.get(analyzer['connections'],airport)['value'],'Destination')['value'] > mp.get(mp.get(analyzer['connections'],lt.getElement(ordered,i))['value'],'Departure')['value'] + mp.get(mp.get(analyzer['connections'],lt.getElement(ordered,i))['value'],'Destination')['value']:
                    lt.insertElement(ordered,airport,i)
                    break
                elif i == lt.size(ordered):
                    lt.addLast(ordered,airport)
                    break
                else:
                    i += 1
    return ordered

#Requerimiento 3
def closestAirport(analyzer,city):
    latitud = float(city['lat'])
    longitud = float(city['lng'])
    list = mp.keySet(analyzer['IATA'])
    minDis = lt.firstElement(list)
    for airport in lt.iterator(list):
        airport_lat = float(mp.get(analyzer['IATA'],airport)['value']['Latitude'])
        airport_lng = float(mp.get(analyzer['IATA'],airport)['value']['Longitude'])
        min_lat = float(mp.get(analyzer['IATA'],minDis)['value']['Latitude'])
        min_lng = float(mp.get(analyzer['IATA'],minDis)['value']['Longitude'])
        if haversine((latitud,longitud),(airport_lat,airport_lng )) < haversine((latitud,longitud),(min_lat,min_lng )):
            minDis = airport
    return minDis

def shortestRoute(analyzer,first_airport,last_airport):
    route = djk.Dijkstra(analyzer['dirigido'],first_airport)
    edge = mp.get(route['visited'],last_airport)['value']['edgeTo']
    distance = mp.get(route['visited'],last_airport)['value']['distTo']
    finalRoute = lt.newList()
    while edge != None:
        lt.addFirst(finalRoute,edge)
        edge = mp.get(route['visited'],edge['vertexA'])['value']['edgeTo']
    return finalRoute,distance



def req_5 (analyzer: dict, param_iata: str) -> dict:
    """
        Dado el código IATA de un aerpouerto, esta función retorna una lista con
        los aeropuertos que se verían afectados en caso de que dicho saliera de funcionamiento.

        Parámetros:
            -> analyzer (dict): analizador.
            -> param_IATA (str): código IATA del aeropuerto.

        Retorno:
            -> (dict): lista que contiene a los aeropuertos que se verían afectados.

    """
    
    # Guardar el grafo 'bigrafo' y el mapa 'IATA'.
    graph = analyzer['dirigido'] 
    mp_iata = analyzer['IATA']

    # Guardar lista de adyacencia del aeropuerto y crear lista de retorno.
    lt_ady = gr.adjacents(graph, param_iata)
    lt_return = lt.newList('ARRAY_LIST')

    # Recorrer los IATA de lt_ady
    for iata in lt.iterator(lt_ady):
        # Obtener la info. del aeropuerto con código pararm_iata y añadirla a lt_return.
        airport_info = mp.get(mp_iata, iata)['value'] 
        lt.addLast(lt_return, airport_info) # 

    return lt_return


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




#####-----#####-----#####-----#####-----#####-----#####   ####---#######---####   #####-----#####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####-----#####   FUNCIONES ADICIONALES   #####-----#####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####-----#####   ####---#######---####   #####-----#####-----#####-----#####-----#####-----#####

"""
    A continuación se definen funciones que serán de utilidad en general.

"""

def fixed_length (input, lenght: int) -> str:
    """
        Dada una cadena de caracteres, esta función permite recotrarla en caso de que
        exceda la longitud necesario (especificada por el parámetro lenght), o adicionarle
        espacios en caso de no ser igual a la longitud necescaria.

        Parámetro:
            -> text (str): cadena que se desea recortar.
            -> lenght (int): longitud a la que se desea ajustar el texto.

        Retorno:
            -> (str): el texo ajustado a la longitud deseada.

    """
    
    # Volver el input una cadena de caracteres.
    text = str(input)

    # Si el texto excede lenght.
    if len(text) > lenght:
        text = text[:lenght -3] + '...'
    
    # Si el texto es menor que lenght.
    elif len(text) < lenght:
        text = (text + " " * lenght)[:lenght]

    # Retorno.
    return(text)