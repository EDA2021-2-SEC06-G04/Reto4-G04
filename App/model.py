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


import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config


# Construccion de modelos
def newcatalog():
    """ Inicializa el catálogo

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
                    'no_dirigido': None,
                    'ciudades': None,
                    'ciudadesnombre': None
                    }

        analyzer['NameAereopuertos'] = mp.newMap(maptype='PROBING',numelements=10000)
        analyzer['IATA'] = mp.newMap(maptype='PROBING',numelements=10000)
        analyzer['dirigido'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=5000,comparefunction=comparerutas)
        analyzer['ciudades'] = mp.newMap(maptype='PROBING',numelements=9000)
        analyzer['ciudadesnombre'] = mp.newMap(maptype='PROBING',numelements=9000)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al catalogo
"""
Agrega un aereopuerto a los grafos y mapas
"""
def addaereopuerto(catalog,aereopuerto):
    mp.put(catalog['IATA'],aereopuerto['IATA'],aereopuerto)
    mp.put(catalog['NameAereopuertos'],aereopuerto['Name'],aereopuerto)    
    gr.insertVertex(catalog['dirigido'],aereopuerto['IATA'])
    if not mp.contains(catalog['ciudades'],aereopuerto['City']):
        mp.put(catalog['ciudades'],aereopuerto['City'],lt.newList(datastructure='ARRAY_LIST'))
    lt.addLast(me.getValue(mp.get(catalog['ciudades'],aereopuerto['City'])),aereopuerto)
    return catalog
"""
Agrega una ciudad al mapa por su nombre
"""
def addciudad(catalog,ciudad):
    if not mp.contains(catalog['ciudadesnombre'],ciudad['city']):
        mp.put(catalog['ciudadesnombre'],ciudad['city'],lt.newList(datastructure='ARRAY_LIST'))
    lt.addLast(me.getValue(mp.get(catalog['ciudadesnombre'],ciudad['city'])),ciudad)
    return catalog

     

"""
Agrega una ruta aérea a los grafos
"""
def addruta(catalog,ruta):
    #vertices = gr.vertices(catalog['dirigido'])
    
    gr.addEdge(catalog['dirigido'],ruta['Departure'],ruta['Destination'],ruta['distance_km'])
    return catalog


# Funciones para creacion de datos

# Funciones de consulta
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

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

# Funciones de comparación
def comparerutas(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1