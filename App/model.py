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
    Esta posee una

"""

# Construccion de modelos
def newcatalog():
    """ 
        Inicializa el catálogo

        dirigido: grafo dirigido con vértices en cada aereopuerto y arcos para
        cada vuelo que los relaciona en la dirección correspondiente.

        no_dirigido: Grafo para representar las relaciones entre aereopuertos de 
        forma que dos aereopuertos se relacionan solo si hay un vuelo directo de ida y otro de vuelta entre ambos.

        ciudades: índice que tiene por llave el nombre de una ciudad y por valor una lista de todas las ciudades diferentes con el nombre.

    """
    try:
        analyzer = {
                    'NameAereopuertos': None,
                    'IATA': None,
                    'dirigido': None,
                    'ciudades': None
                    }

        analyzer['NameAereopuertos'] = mp.newMap(maptype='PROBING',numelements=10000)

        analyzer['IATA'] = mp.newMap(maptype='PROBING',numelements=10000)

        analyzer['dirigido'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=5000,comparefunction=comparerutas)
        analyzer['ciudades'] = mp.newMap(maptype='PROBING',numelements=9000)

        analyzer['routes'] = mp.newMap(numelements=9076,
                                  maptype = 'PROBING')

        analyzer['bigrafo'] = gr.newGraph(datastructure = 'ADJ_LIST',
                                      directed = True,
                                      size = 9076,
                                      comparefunction = compareStopIds)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')




#####-----#####-----#####-----#####-----#####   ###---###----###   #####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####   ADICIÓN DE DATOS   #####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####   ###---###----###   #####-----#####-----######-----####-----#####

"""
    Se definen las funciones que permitirán añadir elementos al catálogo.

"""

def addaereopuerto(catalog,aereopuerto):
    """
        Agrega un aereopuerto a los grafos y mapas

    """
    mp.put(catalog['IATA'],aereopuerto['IATA'],aereopuerto)
    mp.put(catalog['NameAereopuertos'],aereopuerto['Name'],aereopuerto)    
    gr.insertVertex(catalog['dirigido'],aereopuerto['IATA'])
    if not mp.contains(catalog['ciudades'],aereopuerto['City']):
        mp.put(catalog['ciudades'],aereopuerto['City'],lt.newList(datastructure='ARRAY_LIST'))
    lt.addLast(me.getValue(mp.get(catalog['ciudades'],aereopuerto['City'])),aereopuerto)
    return catalog


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


def add_airport (analyzer: dict, airport_id: str) -> None:
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




#####-----#####-----#####-----#####-----#####   ###---####----###   #####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####   CREACIÓN DE DATOS   #####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####   ###---####----###   #####-----#####-----######-----####-----#####

"""
    Se define las funciones que permitirán crear elementos referentes a información
    de interés del catálogo.

"""





#####-----#####-----#####-----#####-----#####   ####---######----####   #####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####   FUNCIONES DE CONSULTA   #####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####   ####---######----####   #####-----#####-----######-----####-----#####

"""
    Se define las funciones que permitirán acceder a información de interés de
    las estructuras.

"""

def totalrutas(catalog):
    """
        Retorna el total de rutas de vuelo (arcos) del grafo

    """
    return gr.numEdges(catalog['dirigido'])



def totalaereopuertos(catalog):
    """
        Retorna el total de aereopuertos (vértices) del grafo

    """ 
    return gr.numVertices(catalog['dirigido'])




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