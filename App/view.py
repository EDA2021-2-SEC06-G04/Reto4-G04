"""
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

#####-----#####-----#####-----#####-----#####-----#####   ####---#####---####   #####-----#####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####-----#####   IMPORTACIÓN MÓDULOS   #####-----#####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####-----#####   ####---#####---####   #####-----#####-----#####-----#####-----#####-----#####

import config as cf
import os
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf




#####-----#####-----#####-----#####-----#####-----#####   #####---######---#####   #####-----#####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####-----#####   FUNCIONES DE IMPRESIÓN   #####-----#####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####-----#####   #####---######---#####   #####-----#####-----#####-----#####-----#####-----#####

"""
    Se definen las funciones que permitirán imprimir el menú y los resultados de cada
    requerimiento, de tal forma que se dispongan de una manera amigable para el usuario.

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




#####-----#####-----#####-----#####-----#####-----#####   ######---######---######   #####-----#####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####-----#####   FUNCIONES CARGA DE DATOS   #####-----#####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####-----#####   ######---######---######   #####-----#####-----#####-----#####-----#####-----#####

"""
    Se definen las funciones que permitirán inicializar el analizador y cargar
    los elementos de la base de datos.

"""

# Función que inicializa el analizador.
def init () -> dict:
    """
        Inicializa el analizador.

        No tiene parámetros.
        
        Retorno:
            -> (dict): el analizador.

    """
    # Crear variable que guarda el analizador y retornarlo.
    analyzer = controller.init()
    return analyzer



# Función que carga todos los datos al analizador.
def load_data (analyzer: dict) -> None:
    """
        Esta función carga todos los datos de interés de la carpeta Data/Skylines.

        Parámetro:
            -> analyzer (dict): analizador.

        No tiene retorno.

    """
    # Cargar los datos mediante la función homónima de controller.py.
    controller.load_data(analyzer)
    controller.loadciudades(analyzer)
    controller.loadaereopuertos(analyzer)
    controller.loadrutas(analyzer)



#####-----#####-----#####-----#####-----#####-----#####   ###---##---###   #####-----#####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####-----#####   MENÚ PRINCIPAL   #####-----#####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####-----#####   ###---##---###   #####-----#####-----#####-----#####-----#####-----#####

"""
    Se define la iteración indefinida que permitirá al usuario cargar la información al catálogo y consultar los
    resultados de cada requerimiento. 

"""

catalog = None       # Crear variable que guardará el catálogo.
os.system('cls')     # Limpiar la consola.

# Ciclo indefinido de la herramienta.
while True:
    
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')

    if int(inputs[0]) == 1:
        print("Creando el catálogo...")
        #catalog es el catálogo que se usará de ahora en adelante
        catalog = controller.init()

    elif int(inputs[0]) == 2:
        print("\nCargando información de rutas de vuelo...")
        controller.load_routes(catalog)
        load_data(catalog)
        numedges = controller.totalrutas(catalog)
        numvertex = controller.totalaereopuertos(catalog)
        print('Numero de aereopuertos en el grafo dirigido: ' + str(numvertex))
        print('Numero de rutas de vuelo en el grafo dirigido: ' + str(numedges))

        numedges = controller.totalrutasnodir(catalog)
        numvertex = controller.totalaereopuertosnodir(catalog)
        print('Numero de aereopuertos en el grafo no dirigido: ' + str(numvertex))
        print('Numero de rutas de vuelo en el grafo no dirigido: ' + str(numedges))
        print('El total de ciudades es de ' + str(mp.size(catalog['ciudades'])))
        primeraereopuerto = controller.loadaereopuertos(catalog)[1]
        print('El primer aereopueto cargado es el de ' + primeraereopuerto['Name'] + ' de la ciudad de ' + primeraereopuerto['City'] + ' de ' + primeraereopuerto['Country'] + ' de latitud ' + primeraereopuerto['Latitude'] + ' y longitud ' + primeraereopuerto['Longitude'] + '.\n')
        ultimaciudad = me.getValue(mp.get(catalog['ciudadesnombre'],lt.lastElement(mp.keySet(catalog['ciudadesnombre']))))
        ultimaciudad = lt.lastElement(ultimaciudad)
        print('La ultima ciudad cargada es ' + ultimaciudad['city'] + ' de población ' + ultimaciudad['population'] + ' de latitud ' + ultimaciudad['lat'] + ' y longitud ' + ultimaciudad['lng'] + '.\n')

    
    # Si escoge la opción 6.
    elif int(inputs[0]) == 6:

        # Limpiar la consola.
        os.system('cls')

        # Imprimir mensaje de carga.
        print("""\n======================= Inputs Req. 4 =======================\n""")
        
        mp_city = catalog['city-id']
        mp_id = catalog['id-city_info']


        first_city = input('Por favor, escriba el nombre de la ciudad inicial:\n  -> ')
        lt_ids = mp.get(mp_city, first_city)['value']

        if (lt.size(lt_ids) == 1):
            id = lt.getElement(lt_ids, 1)
            city = mp.get(mp_id, id)['value']

        else:
            i = 1
            for id in lt.iterator(lt_ids):
                city_info = mp.get(mp_id, id)['value']
                city_name = city_info['city']
                city_country = city_info['country']

                print(str(i) + ' - ' + city_name + "," + city_country)
                i += 1
            
            id = int(input('Por favor, digite el número de la ciudad que desea escoger:\n  ->'))
            first_city = mp.get(mp_id, lt.getElement(lt_ids, id))['value']


        last_city = input('Por favor, escriba el nombre de la ciudad final:\n  -> ')
        lt_ids = mp.get(mp_city, last_city)['value']

        if (lt.size(lt_ids) == 1):
            id = lt.getElement(lt_ids, 1)
            city_info = mp.get(mp_id, id)['value']

        else:
            i = 1
            for id in lt.iterator(lt_ids):
                city_info = mp.get(mp_id, id)['value']
                city_name = city_info['city']
                city_country = city_info['country']
                print(str(i) + ' - ' + city_name + "," + city_country)
                i += 1
            id = int(input('Por favor, digite el número de la ciudad que desea escoger:\n  ->'))
            last_city = mp.get(mp_id, lt.getElement(lt_ids, id))['value']





    else:
        sys.exit(0)
sys.exit(0)
