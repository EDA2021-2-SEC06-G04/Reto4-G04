"""
Por hacer:
 1- Ver si es necesario añadir estructura que contenga los aeropuertos (tabla de Hash).
 2- Crear función que agrega vértices.
 3- Crear función que agrega arcos entre nodos.
 4- 

"""

import config as cf
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert cf

import csv

### MODEL ###
def new_analyzer () -> dict:
    analyzer = {}
    analyzer['routes'] = m.newMap(numelements=9076,
                                  maptype = 'PROBING')

    analyzer['bigrafo'] = gr.newGraph(datastructure = 'ADJ_LIST',
                                      directed = True,
                                      size = 9076,
                                      comparefunction = compareStopIds)
    return analyzer

def mp_add_route (analyzer: dict, departure: str, destination:str, distance: float) -> None:
    
    mp_routes = analyzer['routes']
    exists = m.contains(mp_routes, departure)

    if exists:

        mp_destinatios = m.get(mp_routes, departure)['value']
        m.put(mp_destinatios, destination, distance)

    else:
        new_mp_destinatios = m.newMap(maptype = 'PROBING')
        m.put(new_mp_destinatios, destination, distance)
        m.put(mp_routes, departure, new_mp_destinatios)


def add_airport (analyzer: dict, airport_id: str) -> None:
    if not (gr.containsVertex(analyzer['bigrafo'], airport_id)):
        gr.insertVertex(analyzer['bigrafo'], airport_id)


def add_route (analyzer: dict, origin: str, destination: str, distance: float) -> None:
    edge = gr.getEdge(analyzer['bigrafo'], origin, destination)
    if (edge == None):
        gr.addEdge(analyzer['bigrafo'], origin, destination, distance)

def compareStopIds(stop, keyvaluestop):
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1

### CONTROLLER ###
def init() -> None:
    analyzer = new_analyzer()
    return analyzer

def load_routes (analyzer: dict) -> None:
    file = cf.data_dir + '\\Skylines\\routes_full.csv'
    input_file = csv.DictReader(open(file, encoding='utf-8'))

    for route in input_file:
        
        departure = route['Departure']
        destination = route['Destination']
        distance = float(route['distance_km'])

        mp_add_route(analyzer, departure, destination, distance)

    mp_routes = analyzer['routes']
    
    for destination in (lt.iterator(m.keySet(mp_routes))):
        mp_departures = m.get(mp_routes, destination)['value']
        for departure in (lt.iterator(m.keySet(mp_departures))):
            if (m.contains(mp_routes, departure)):
                mp_departure_departures = m.get(mp_routes, departure)['value']
                if m.contains(mp_departure_departures, destination):
                    add_airport(analyzer, departure)
                    add_airport(analyzer, destination)
                    add_route(analyzer, departure, destination, distance)

analyzer = init()
load_routes(analyzer)
print(gr.numVertices(analyzer['bigrafo']))
print(gr.numEdges(analyzer['bigrafo']))
