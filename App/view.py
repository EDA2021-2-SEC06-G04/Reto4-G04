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
import time
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

# Función que imprime el menú de opciones.
def print_menu () -> None:
    """
        Esta función imprime el menú de interacción con el usuario.
        
        No tiene ni parámetros ni retorno.

    """
    
    print("""\n======================= BIENVENIDO =======================\n""")
    print("  1- Cargar información al analizador.")
    print("  2- (Req. 1) Encontrar puntos de interconexión aérea.")
    print("  3- (Req. 2) Encontrar clústeres de tráfico aéreo.")
    print("  4- (Req. 3) Encontrar la ruta más corta entre ciudades.")
    print("  5- (Req. 4) Utilizar las millas de viajero.")
    print("  6- (Req. 5) Cuantificar el efecto de un aeropuerto cerrado.")
    print("  7- (Req. 6) Comparar con servicio WEB externo.")
    print("  8- (Req. 7) Visualizar gráficamente los requerimientos.")
    print("  0- Salir.")




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



#####-----#####-----#####-----#####-----#####-----#####   ###---##---###   #####-----#####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####-----#####   MENÚ PRINCIPAL   #####-----#####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####-----#####   ###---##---###   #####-----#####-----#####-----#####-----#####-----#####

"""
    Se define la iteración indefinida que permitirá al usuario cargar la información al catálogo y consultar los
    resultados de cada requerimiento. 

"""

analyzer = None      # Crear variable que guardará el catálogo.
os.system('cls')     # Limpiar la consola.

# Ciclo indefinido de la herramienta.
while True:
    
    # Imprimir menú y preguntar al usuario la acción que desea realizar.
    print_menu()
    inputs = input('\nPor favor, seleccione una opción para continuar:\n  -> ')

    # Si el usuario ingresó una opción válida.
    try:

        # Opción carga de datos.
        if int(inputs[0]) == 1:

            # Limpiar la consola.
            os.system('cls')
            
            # Imprimir mensaje de carga.
            print("""\n======================= Carga de Datos =======================\n""")
            print("Cargando información al catálogo ...")

            analyzer = init ()                   # Inicializar catálogo.
            start_time = time.process_time()     # Iniciar el tiempo
            load_data(analyzer)                  # Cargar datos al catálogo.
            stop_time = time.process_time()      # Parar el tiempo.

            # Calcular tiempo de ejecución en milisegundos.
            elapsed_time_mseg = (stop_time - start_time)*1000

            # Imprimir mensaje de éxito.
            print("\n<> Información cargada con éxito. <>")
            print(' - ' + "Tiempo de ejecución:", elapsed_time_mseg, "milisegundos.")

            numedges = controller.total_routes(analyzer)
            numvertex = controller.total_airports(analyzer)
            print(' - ' + 'Número de aereopuertos en el grafo dirigido: ' + str(numvertex) + '.')
            print(' - ' + 'Número de rutas de vuelo en el grafo dirigido: ' + str(numedges) + '.')

            numedges = controller.no_dir_total_routes(analyzer)
            numvertex = controller.nor_dir_total_airports(analyzer)
            print(' - ' + 'Numero de aereopuertos en el grafo no dirigido: ' + str(numvertex) + '.')
            print(' - ' + 'Numero de rutas de vuelo en el grafo no dirigido: ' + str(numedges) + '.')
            print(' - ' + 'El total de ciudades es de ' + str(mp.size(analyzer['ciudades'])) + '.')

            primeraereopuerto = controller.loadaereopuertos(analyzer)[1]
            print(' - ' + 'El primer aereopueto cargado es el de', primeraereopuerto['Name'], 'de la ciudad de', primeraereopuerto['City'], 'de',
                  primeraereopuerto['Country'], 'de latitud', round(float(primeraereopuerto['Latitude']), 2), 'y longitud', str(round(float(primeraereopuerto['Longitude']), 2)) + '.')

            #ultimaciudad = me.getValue(mp.get(catalog['ciudadesnombre'],lt.lastElement(mp.keySet(catalog['ciudadesnombre']))))
            #ultimaciudad = lt.lastElement(ultimaciudad)
            #print(' - ' + 'La ultima ciudad cargada es ' + ultimaciudad['city'] + ' de población ' + ultimaciudad['population'] + ' de latitud',
            #      round(float(ultimaciudad['lat']), 2), 'y longitud', str(round(float(ultimaciudad['lng']) ,2)) + '.')

        
        # Si escoge la opción 6.
        elif int(inputs[0]) == 6:

            # Limpiar la consola.
            os.system('cls')

            # Imprimir mensaje de carga.
            print("""\n======================= Inputs Req. 4 =======================\n""")
            
            # Guardar mapas de interés.
            mp_city = analyzer['city-id']
            mp_id = analyzer['id-city_info']

            # Pedir al usuario la primera ciudad y obtener la lista de ids de la ciudad con dicho nombre.
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



        # Opción salir.
        elif int(inputs[0]) == 0:
            
            # Limpiar la consola.
            os.system('cls')
            
            # Imprimir mensaje de carga.
            print("""\n======================= Exit =======================\n""")
            print("Gracias por usar la herramienta. Hasta pronto.\n\n")

            sys.exit(0)



        # Si se ingresa un valor erróneo.
        else:
            os.system('cls')        # Limpiar la consola.
            print("""\n======================= ERROR =======================\n""")
            print("Debe ingresar una opción válida.\n\n")
            sys.exit(0)



    # Si el usuario ingresó una opción inválida.
    except ValueError:
        os.system('cls')    # Limpiar la consola.
        print("""\n======================= ERROR =======================\n""")
        print("Debe ingresar valores adecuados.\n\n")
        sys.exit(0)

sys.exit(0)