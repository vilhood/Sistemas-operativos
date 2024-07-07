from Scheduling import fcfs, spn, srt, hrrn, round_robin
from Fetch.fetch import actual

"""
NOTA: si inicia una sola instancia global de la clase de fetch - Rdy

Se guardan los procesos en este formato : [] -> (<comando>,<tiempo inicio>,<tiempo estimado>), luego,obtiene 
el algoritmo de planificación que recibe del usuario, y usa la función de la clase de fetch Execute([],<algoritmo>) - Rdy

Para repetir, recibe el id de la ejecución, lo ingresa al metodo de la clase fetch repeat(<id>), finalmente 
manda el resultado de esa función junto con el algoritmo especificado al scheduling -Rdy

Para ver todas las ejecuciones simplemente usar el metodo get_all_executions() de la clase de fetch - Rdy
"""

def obtener_comandos():
    comandos = []
    n = int(input("Ingrese el número de comandos: "))
    for i in range(n):
        cmd = input(f"Ingrese el nombre del comando {i+1}: ")
        tiempo_lleg = int(input(f"Ingrese el tiempo de llegada del comando {i+1}: "))
        tiempo_raf = int(input(f"Ingrese el tiempo de ráfaga del comando {i+1}: "))
        comandos.append((cmd, tiempo_lleg, tiempo_raf))
    return comandos

# def obtener_imagenes(comandos):
#     imagenes = {}
#     for cmd, _, _ in comandos:
#         img = input(f"Ingrese la imagen para el comando {cmd}: ")
#         imagenes[cmd] = [img]
#     return imagenes

def procesar_resultados(resultados, algoritmo, imagenes):
    if algoritmo == 'fcfs':
        return fcfs(resultados, imagenes)
    elif algoritmo == 'spn':
        return spn(resultados, imagenes)
    elif algoritmo == 'srt':
        return srt(resultados, imagenes)
    elif algoritmo == 'hrrn':
        return hrrn(resultados, imagenes)
    elif algoritmo == 'round_robin':
        quantum = int(input("Ingrese el quantum para Round Robin: "))
        return round_robin(resultados, imagenes, quantum=quantum)
    else:
        raise ValueError("Algoritmo de planificación no reconocido")

# Preguntar al usuario la acción que desea realizar
opcion = input("¿Desea ingresar nuevos comandos,repetir una ejecución o ver todas las ejecuciones?(ingresar/repetir/ver): ").strip().lower()

if opcion == 'ingresar':
    comandos = obtener_comandos()

    algoritmo = input("Ingrese el algoritmo de planificación (fcfs, spn, srt, hrrn, round_robin): ").strip().lower()
    # imagenes = obtener_imagenes(comandos)
    comandos, diccionario = actual.Execute(comandos, algoritmo)

    resultados_finales = procesar_resultados(comandos, algoritmo, diccionario)
    print(resultados_finales)

elif opcion == 'repetir':
    id_ejecucion = int(input("Ingrese el ID de la ejecución a repetir: "))

    comandos, diccionario = actual.repeat_execution(id_ejecucion)
    # imagenes = obtener_imagenes(resultados_repetidos[0])

    algoritmo = input("Ingrese el algoritmo de planificación (fcfs, spn, srt, hrrn, round_robin): ").strip().lower()

    resultados_finales_repetidos = procesar_resultados(comandos, algoritmo, diccionario)
    print(resultados_finales_repetidos)

elif opcion == 'ver':
    ejecuciones = actual.get_all_executions()
    for ejecucion in ejecuciones:
        print(ejecucion)

else:
    print("Opción no válida. Por favor, ingrese 'ingresar', 'repetir' o 'ver'.")
