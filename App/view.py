﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf

rutasfile = 'routes_full.csv'
aereopuertosfile = 'airports_full.csv'
ciudadesfile = 'worldcities.csv'

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Crear el catálogo")
    print("2- Cargar información en el catálogo")
    print("3- Encontrar puntos de interconexión aérea")
    print("4- Encontrar clústeres de tráfico aéreo")
    print("5- Encontrar la ruta más corta entre ciudades")
    print("6- Utilizar las millas de viajero")
    print("7- Cuantificar el efecto de un aeropuerto cerrado")
    print("8- Comparar con servicio WEB externo")
    print("9- Visualizar gráficamente los requerimientos")


catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Creando el catálogo...")
        #catalog es el catálogo que se usará de ahora en adelante
        catalog = controller.init()

    elif int(inputs[0]) == 2:
        print("\nCargando información de rutas de vuelo...")
        controller.loadciudades(catalog, ciudadesfile)
        controller.loadaereopuertos(catalog, aereopuertosfile)
        controller.loadrutas(catalog, rutasfile)
        numedges = controller.totalrutas(catalog)
        numvertex = controller.totalaereopuertos(catalog)
        print('Numero de aereopuertos en el grafo dirigido: ' + str(numvertex))
        print('Numero de rutas de vuelo en el grafo dirigido: ' + str(numedges))
        print('El total de ciudades es de ' + str(mp.size(catalog['ciudades'])))
        primeraereopuerto = me.getValue(mp.get(catalog['IATA'],lt.firstElement(mp.keySet(catalog['IATA']))))
        print('El primer aereopueto cargado es el de ' + primeraereopuerto['Name'] + ' de la ciudad de ' + primeraereopuerto['City'] + ' de ' + primeraereopuerto['Country'] + ' de latitud ' + primeraereopuerto['Latitude'] + ' y longitud ' + primeraereopuerto['Longitude'] + '.\n')
        ultimaciudad = me.getValue(mp.get(catalog['ciudadesnombre'],lt.lastElement(mp.keySet(catalog['ciudadesnombre']))))
        ultimaciudad = lt.lastElement(ultimaciudad)
        print('La ultima ciudad cargada es ' + ultimaciudad['city'] + ' de población ' + ultimaciudad['population'] + ' de latitud ' + ultimaciudad['lat'] + ' y longitud ' + ultimaciudad['lng'] + '.\n')
    else:
        sys.exit(0)
sys.exit(0)
