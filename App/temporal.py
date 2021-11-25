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
    
    analyzer['bigrafo'] = gr.newGraph(datastructure = 'ADJ_LIST',
                                      directed = False,
                                      size = 9076)

    return analyzer

def add_airport (analyzer: dict, airport_id: str) -> None:
    if not (gr.containsVertex(analyzer['bigrafo'], airport_id)):
        gr.insertVertex(analyzer['bigrafo'], airport_id)

def add_route (analyzer, origin, destination) -> None:
    edge = gr.getEdge(analyzer['bigrafo'], origin, destination)
    if (edge == None):
        gr.addEdge(analyzer['bigtafo'], origin, destination, 0)

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

        add_airport(analyzer, departure)
        add_airport(analyzer, destination)
        add_route(analyzer, departure, destination)