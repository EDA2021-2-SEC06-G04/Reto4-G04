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

#####-----#####-----#####-----#####-----#####-----#####   ####---#####---####   #####-----#####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####-----#####   IMPORTACIÓN MÓDULOS   #####-----#####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####-----#####   ####---#####---####   #####-----#####-----#####-----#####-----#####-----#####

#from DISClib.ADT.graph import edges
import config as cf
import os
import time
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import graph as gr
from DISClib.DataStructures import mapentry as me
from haversine import haversine
assert cf




#####-----#####-----#####-----#####-----#####-----#####   #####---######---#####   #####-----#####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####-----#####   FUNCIONES DE IMPRESIÓN   #####-----#####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####-----#####   #####---######---#####   #####-----#####-----#####-----#####-----#####-----#####

"""
    Se definen las funciones que permitirán imprimir el menú y los resultados de cada
    requerimiento, de tal forma que se dispongan de una manera amigable para el usuario.

"""
sys.setrecursionlimit(2 ** 20)

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



def print_reqs (lt_print: dict) -> None:
    # Imprimir header.
    print("#" * 120)
    print("# ", end = " ")
    print(fixed_length('IATA', 4), end = " # ")
    print(fixed_length('Name', 40), end = " # ")
    print(fixed_length('City', 31), end = " # ")
    print(fixed_length('Country', 31), end = " # ")
    print()
    print("#" * 120)

    for element in lt.iterator(lt_print):
        iata = element['IATA']
        name = element['Name']
        city = element['City']
        country = element['Country']

        print("# ", end = " ")
        print(fixed_length(iata, 4), end = " # ")
        print(fixed_length(name, 40), end = " # ")
        print(fixed_length(city, 31), end = " # ")
        print(fixed_length(country, 31), end = " # ")
        print()



def print_req_5 (lt_ady: dict, param_iata: str) -> None:
    """
        Esta función imprime la respuesta del requerimiento 5 de una manera amigable para el usuario.

        Parámetros:
            -> lt_ady (dict): lista de adyacencias.
            -> param_iata (str): aeropuerto a consultar.

        No tiene retorno.

    """
    size = lt.size(lt_ady)

    print('En total, habrían', size, 'aeropuertos que se verían afectados en caso de que el aeropuerto',
           param_iata, 'dejara de funcionar.')
    print('Una muestra de la información de algunos de estos se dispone a continuación:\n')


    if (size > 6):
        new_lt = lt.newList('ARRAY_LIST')
        lt.addLast(new_lt, lt.getElement(lt_ady, 1))
        lt.addLast(new_lt, lt.getElement(lt_ady, 2))
        lt.addLast(new_lt, lt.getElement(lt_ady, 3))
        lt.addLast(new_lt, lt.getElement(lt_ady, size - 2))
        lt.addLast(new_lt, lt.getElement(lt_ady, size - 1))
        lt.addLast(new_lt, lt.getElement(lt_ady, size))
        print_reqs(new_lt)

    else:
        print_reqs(lt_ady)
    
    print("#" * 120)
    print()



def print_req_2 (ans: tuple, iara_1, iara_2) -> None:
    connected , strongly_con, lt_airports = ans
    are_str_con = 'sí' if (strongly_con == True) else 'no'
    print('La cantidad de clústeres presentes en la red de transporte aéreo es:', str(connected) + '.')
    print('Los aeropuertos', iara_1, 'y', iara_2, are_str_con, 'se encuentran en el mismo clúster.')
    print('La información acerca de los dos aeropuetos buscados se dispone a continuación:\n')
    print_reqs(lt_airports)
    print("#" * 120)
    print()




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




#####-----#####-----#####-----#####-----#####   ####---######----####   #####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####   FUNCIONES DE CONSULTA   #####-----#####-----#####-----#####-----#####
#####-----#####-----#####-----#####-----#####   ####---######----####   #####-----#####-----######-----####-----#####

"""
    Se define las funciones que permitirán acceder a información de interés de
    las estructuras.

"""

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
    lt_return = controller.req_5(analyzer, param_iata)
    return (lt_return)



def req_2 (analyzer: dict, iata_1: str, iata_2: str) -> tuple:
    return controller.req_2(analyzer, iata_1, iata_2)




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
    text = controller.fixed_length(input, lenght)
    return text



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
            primeraereopuerto,ultimoaereopuerto = controller.loadaereopuertos(analyzer)
            load_data(analyzer)                  # Cargar datos al catálogo.
            stop_time = time.process_time()      # Parar el tiempo.

            # Calcular tiempo de ejecución en milisegundos.
            elapsed_time_mseg = (stop_time - start_time)*1000

            # Imprimir mensaje de éxito.
            print("\n<> Información cargada con éxito. <>")
            print(' - ' + "Tiempo de ejecución:", elapsed_time_mseg, "milisegundos.")

            numedges = controller.total_routes(analyzer)
            numvertex = controller.total_airports(analyzer)
            print(' - Número de aereopuertos totales: ' + str(mp.size(analyzer['IATA'])))
            print(' - ' + 'Número de aereopuertos en el grafo dirigido: ' + str(numvertex) + '.')
            print(' - ' + 'Número de rutas de vuelo en el grafo dirigido: ' + str(numedges) + '.')

            numedges = controller.no_dir_total_routes(analyzer)
            numvertex = controller.nor_dir_total_airports(analyzer)
            print(' - ' + 'Numero de aereopuertos en el grafo no dirigido: ' + str(numvertex) + '.')
            print(' - ' + 'Numero de rutas de vuelo en el grafo no dirigido: ' + str(numedges) + '.')
            print(' - ' + 'El total de ciudades es de ' + str(lt.size(analyzer['lt_cities'])) + '.')

            print(' - ' + 'El primer aereopueto cargado es el de', primeraereopuerto['Name'], 'de la ciudad de', primeraereopuerto['City'], 'de',
                  primeraereopuerto['Country'], 'de latitud', round(float(primeraereopuerto['Latitude']), 2), 'y longitud', str(round(float(primeraereopuerto['Longitude']), 2)) + '.')
            print(' - ' + 'El primer aereopueto cargado es el de', ultimoaereopuerto['Name'], 'de la ciudad de', ultimoaereopuerto['City'], 'de',
                  ultimoaereopuerto['Country'], 'de latitud', round(float(ultimoaereopuerto['Latitude']), 2), 'y longitud', str(round(float(ultimoaereopuerto['Longitude']), 2)) + '.')

            lt_cities = analyzer['lt_cities']
            last_city = lt.lastElement(lt_cities)
            print(' - ' + 'La ultima ciudad cargada es ' + last_city['city'] + ' de población ' + str(last_city['population']) + ' de latitud',
                  round(float(last_city['lat']), 2), 'y longitud', str(round(float(last_city['lng']) ,2)) + '.')

        elif int(inputs[0]) == 2:
            # Iniciar el tiempo.
            start_time = time.process_time()
            interconnections = controller.interconnections(analyzer)
            print('Los 5 aereopuertos más conectados son: \n')
            for airport in lt.iterator(interconnections):
                dicc = mp.get(analyzer['IATA'],airport)['value']
                outbound = mp.get(mp.get(analyzer['connections'],airport)['value'],'Departure')['value']
                inbound = mp.get(mp.get(analyzer['connections'],airport)['value'],'Destination')['value']
                connections = outbound + inbound

                print('Nombre: ' + dicc['Name'] + '      Ciudad: ' + dicc['City'] + '      País: ' + dicc['Country'] + '      IATA: ' + airport + '      Conexiones: ' + str(connections) + '      Conexiones entrantes: ' + str(inbound) + '      Conexiones salientes: ' + str(outbound) + '\n')
            print('El número de aereopuertos conectados es de ' + str(controller.total_airports(analyzer)) + '\n')
            print('El número de aereopuertos en la red es de ' + str(mp.size(analyzer['IATA'])) )
            # Parar el tiempo.
            stop_time = time.process_time()

            # Calcular tiempo de ejecución en milisegundos e imprimirlo.
            elapsed_time_mseg = (stop_time - start_time) * 1000
            print("Tiempo de ejecución del requerimiento:", elapsed_time_mseg, "milisegundos.\n")


        
        # Si escoge la opción 3.
        elif int(inputs[0]) == 3:

            # Limpiar la consola.
            os.system('cls')

            # Imprimir mensaje de carga.
            print("""\n======================= Inputs Req. 2 =======================\n""")
                
            # Preguntar al usuario por inputs.
            param_iata_1 = input('Por favor, escriba el código IATA del primer aeropuerto:\n  -> ')
            param_iata_2 = input('Por favor, escriba el código IATA del segundo aeropuerto:\n  -> ')

            # Imprimir mensaje de carga.
            print("""\n====================== Outputs Req. 2 =======================\n""")

            # Iniciar el tiempo.
            start_time = time.process_time()

            # Guardar respuesta del requerimiento 3.
            ans_req_2 = req_2(analyzer, param_iata_1, param_iata_2)

            # Parar el tiempo.
            stop_time = time.process_time()

            # Calcular tiempo de ejecución en milisegundos e imprimirlo.
            elapsed_time_mseg = (stop_time - start_time) * 1000
            print("Tiempo de ejecución del requerimiento:", elapsed_time_mseg, "milisegundos.\n")

            # Imprimir respuesta.
            print_req_2(ans_req_2, param_iata_1, param_iata_2)



        # Si escoge la opción 4.
        elif int(inputs[0]) == 4:

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
                first_city = mp.get(mp_id, id)['value']

            else:
                i = 1
                for id in lt.iterator(lt_ids):
                    city_info = mp.get(mp_id, id)['value']
                    city_name = city_info['city']
                    city_country = city_info['country']

                    print(str(i) + ' - ' + city_name + ", " + city_country)
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
                    print(str(i) + ' - ' + city_name + ", " + city_country)
                    i += 1
                id = int(input('Por favor, digite el número de la ciudad que desea escoger:\n  ->'))
                last_city = mp.get(mp_id, lt.getElement(lt_ids, id))['value']
            
            # Iniciar el tiempo.
            start_time = time.process_time()

            first_airport = controller.closestAirport(analyzer,first_city)
            last_airport = controller.closestAirport(analyzer,last_city)
            route,distance = controller.shortestRoute(analyzer,first_airport,last_airport)
            first_airport = mp.get(analyzer['IATA'],first_airport)['value']
            last_airport = mp.get(analyzer['IATA'],last_airport)['value']
            print('\nEl aereopuerto desde el que se va a partir es:',first_airport['Name'], 'de la ciudad de', first_airport['City'], 'de',
                  first_airport['Country'],'con código IATA (',first_airport['IATA'],')\n')
            print('El aereopuerto al que se va a llegar es:',last_airport['Name'], 'de la ciudad de', last_airport['City'], 'de',
                  last_airport['Country'],'con código IATA (',last_airport['IATA'],')\n')
            print('La distancia total de la ruta de viaje será de:',str(distance),'kilómetros de vuelo\n')
            routeAirports = lt.newList(datastructure='ARRAY_LIST')      
            print('Los arcos del camino más corto serán: \n')
            for edge in lt.iterator(route):
                lt.addLast(routeAirports,edge['vertexA'])
                print('Aereopuerto de salida:',edge['vertexA'],'    Aereopuerto de llegada:',edge['vertexB'],'    Distancia del vuelo:',edge['weight'],)
            lt.addLast(routeAirports,last_airport['IATA'])
            print('\nLos paradas de toda la ruta serán:\n')
            for airport in lt.iterator(routeAirports):
                info = mp.get(analyzer['IATA'],airport)['value']
                print('Nombre del aereopuerto:',info['Name'],'    Ciudad:',info['City'],'    País:',info['Country'],'    Código IATA:',info['IATA'],'\n')
            fst_lat = float(first_airport['Latitude'])
            lst_lat = float(last_airport['Latitude'])                  
            fst_lng = float(first_airport['Longitude'])
            lst_lng = float(last_airport['Longitude'])
            print('La distancia total entre aereopuertos será de,',str(round(haversine((fst_lat,fst_lng),(lst_lat,lst_lng)),3)),'kilómetros, mientras que la distancia total entre ciudades será de',str(round(haversine((first_city['lat'],first_city['lng']),(last_city['lat'],last_city['lng'])),3)),'kilómetros.')
            # Parar el tiempo.
            stop_time = time.process_time()

            # Calcular tiempo de ejecución en milisegundos e imprimirlo.
            elapsed_time_mseg = (stop_time - start_time) * 1000
            print("Tiempo de ejecución del requerimiento:", elapsed_time_mseg, "milisegundos.\n")

        # Si escoge la opción 5.
        elif int(inputs[0]) == 5:
            # Limpiar la consola.
            os.system('cls')

            # Imprimir mensaje de carga.
            print("""\n======================= Inputs Req. 4 =======================\n""")

             # Preguntar al usuario por inputs.
            param_iata = input('Por favor, escriba el código IATA del aeropuerto inicial:\n  -> ')
            available_miles = float(input('Por favor, escriba el número de millas disponibles:\n  -> '))

            # Imprimir mensaje de carga.
            print("""\n====================== Outputs Req. 4 =======================\n""")

            # Iniciar el tiempo.
            start_time = time.process_time()

            GraphMST = controller.MST(analyzer,param_iata)



        # Si escoge la opción 6.
        elif int(inputs[0]) == 6:

            # Limpiar la consola.
            os.system('cls')

            # Imprimir mensaje de carga.
            print("""\n======================= Inputs Req. 5 =======================\n""")
                
            # Preguntar al usuario por inputs.
            param_iata = input('Por favor, escriba el código IATA del aeropuerto fuera de funcionamiento:\n  -> ')

            # Imprimir mensaje de carga.
            print("""\n====================== Outputs Req. 5 =======================\n""")

            # Iniciar el tiempo.
            start_time = time.process_time()

            # Guardar respuesta del requerimiento 3.
            ans_req_5 = req_5(analyzer, param_iata)

            # Parar el tiempo.
            stop_time = time.process_time()

            # Calcular tiempo de ejecución en milisegundos e imprimirlo.
            elapsed_time_mseg = (stop_time - start_time) * 1000
            print("Tiempo de ejecución del requerimiento:", elapsed_time_mseg, "milisegundos.\n")

            # Imprimir respuesta.
            print_req_5(ans_req_5, param_iata)


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