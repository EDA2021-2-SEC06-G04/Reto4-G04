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
                    'aereopuertos': None,
                    'dirigido': None,
                    'no_dirigido': None,
                    'ciudades': None
                    }

        analyzer['aereopuertos'] = lt.newList(datastructure='ARRAY_LIST')
        analyzer['dirigido'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=5000,comparefunction=comparerutas
                                              )
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al catalogo
"""
Agrega una ruta aérea a los grafos
"""
def addruta(catalog,ruta):
    #vertices = gr.vertices(catalog['dirigido'])
    if not (lt.isPresent(catalog['aereopuertos'],ruta['Departure'])):
        gr.insertVertex(catalog['dirigido'],ruta['Departure'])
        lt.addLast(catalog['aereopuertos'],ruta['Departure'])
    if not (lt.isPresent(catalog['aereopuertos'],ruta['Destination'])):
        gr.insertVertex(catalog['dirigido'],ruta['Destination'])
        lt.addLast(catalog['aereopuertos'],ruta['Destination']) 
    gr.addEdge(catalog['dirigido'],ruta['Departure'],ruta['Destination'],ruta['distance_km'])
    return catalog


# Funciones para creacion de datos

# Funciones de consulta

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