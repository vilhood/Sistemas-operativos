import time
import subprocess
import threading

def ejecutar_contenedor(img, tiempo):
    proceso = subprocess.Popen(f"docker run --rm {img}", shell=True)
    time.sleep(tiempo)
    proceso.terminate()

def ejecutar_comando(cmd, tiempo):
    ejecutar_contenedor(cmd, tiempo)

def responses(tiempos_fin, tiempos_resp, prom_fin, prom_resp):
    return {
        'tiempos_fin': tiempos_fin,
        'tiempos_resp': tiempos_resp,
        'prom_fin': prom_fin,
        'prom_resp': prom_resp
    }

# Algoritmo FCFS
def fcfs(cmds, imgs):
    prom_fin = 0
    prom_resp = 0
    tiempos_fin = []
    tiempos_resp = []
    tiempo_act = 0
    for cmd, tiempo_lleg, tiempo_raf in cmds:
        if tiempo_act < tiempo_lleg:
            tiempo_act = tiempo_lleg
        hilo = threading.Thread(target=ejecutar_comando, args=(imgs[cmd]['image_id'], tiempo_raf))
        hilo.start()
        hilo.join(tiempo_raf)
        tiempo_fin = tiempo_act + tiempo_raf - tiempo_lleg
        tiempo_resp = tiempo_act - tiempo_lleg
        tiempos_fin.append(tiempo_fin)
        tiempos_resp.append(tiempo_resp)
        prom_fin += tiempo_fin
        prom_resp += tiempo_resp
        print(f"FCFS - Cmd: {cmd}, Tiempo Fin: {tiempo_fin}, Tiempo Resp: {tiempo_resp}")
        tiempo_act += tiempo_raf
    prom_fin = round(prom_fin / len(cmds), 3)
    prom_resp = round(prom_resp / len(cmds), 3)

    print(f"Promedio de tiempo de finalización: {prom_fin}")
    print(f"Promedio de tiempo de respuesta: {prom_resp}")

    return responses(tiempos_fin, tiempos_resp, prom_fin, prom_resp)

# Algoritmo SPN
def spn(cmds, imgs):
    tiempo_act = 0
    cola = []
    tiempos_fin = []
    tiempos_resp = []
    prom_fin = 0
    prom_resp = 0
    cmds_copia = cmds.copy()
    while cmds or cola:
        while cmds and cmds[0][1] <= tiempo_act:
            cola.append(cmds.pop(0))
        if cola:
            cola.sort(key=lambda x: x[2])
            cmd, tiempo_lleg, tiempo_raf = cola.pop(0)
            hilo = threading.Thread(target=ejecutar_comando, args=(imgs[cmd]['image_id'], tiempo_raf))
            hilo.start()
            hilo.join(tiempo_raf)
            tiempo_fin = tiempo_act + tiempo_raf - tiempo_lleg
            tiempo_resp = tiempo_act - tiempo_lleg
            tiempos_fin.append(tiempo_fin)
            tiempos_resp.append(tiempo_resp)
            prom_fin += tiempo_fin
            prom_resp += tiempo_resp
            print(f"SPN - Cmd: {cmd}, Tiempo Fin: {tiempo_fin}, Tiempo Resp: {tiempo_resp}")
            tiempo_act += tiempo_raf
        else:
            tiempo_act += 1
    prom_fin = round(prom_fin / len(cmds_copia), 3)
    prom_resp = round(prom_resp / len(cmds_copia), 3)

    print(f"Promedio de tiempo de finalización: {prom_fin}")
    print(f"Promedio de tiempo de respuesta: {prom_resp}")

    return responses(tiempos_fin, tiempos_resp, prom_fin, prom_resp)

# Algoritmo SRT
def srt(cmds, imgs):
    tiempo_act = 0
    cola = []
    tiempos_fin = []
    tiempos_resp = []
    prom_fin = 0
    prom_resp = 0
    cmds_copia = cmds.copy()
    tiempos_raf = {i: tiempo_raf for i, (_, _, tiempo_raf) in enumerate(cmds)}
    while cmds or cola:
        while cmds and cmds[0][1] <= tiempo_act:
            cola.append(cmds.pop(0))
        if cola:
            cola.sort(key=lambda x: tiempos_raf[x[0]])
            cmd, tiempo_lleg, tiempo_raf = cola.pop(0)
            idx = list(tiempos_raf.keys())[list(tiempos_raf.values()).index(tiempo_raf)]
            quantum = 1
            hilo = threading.Thread(target=ejecutar_comando, args=(imgs[cmd]['image_id'], quantum))
            hilo.start()
            hilo.join(quantum)
            tiempo_restante = tiempo_raf - quantum
            if tiempo_restante > 0:
                cola.append((cmd, tiempo_lleg, tiempo_restante))
                tiempos_raf[idx] -= quantum
            else:
                tiempo_fin = tiempo_act + tiempo_raf - tiempo_lleg
                tiempo_resp = tiempo_act - tiempo_lleg
                tiempos_fin.append(tiempo_fin)
                tiempos_resp.append(tiempo_resp)
                prom_fin += tiempo_fin
                prom_resp += tiempo_resp
                print(f"SRT - Cmd: {cmd}, Tiempo Fin: {tiempo_fin}, Tiempo Resp: {tiempo_resp}")
            tiempo_act += quantum
        else:
            tiempo_act += 1
    prom_fin = round(prom_fin / len(cmds_copia), 3)
    prom_resp = round(prom_resp / len(cmds_copia), 3)

    print(f"Promedio de tiempo de finalización: {prom_fin}")
    print(f"Promedio de tiempo de respuesta: {prom_resp}")

    return responses(tiempos_fin, tiempos_resp, prom_fin, prom_resp)

# Algoritmo HRRN
def hrrn(cmds, imgs):
    tiempo_act = 0
    cola = []
    tiempos_fin = []
    tiempos_resp = []
    prom_fin = 0
    prom_resp = 0
    cmds_copia = cmds.copy()
    while cmds or cola:
        while cmds and cmds[0][1] <= tiempo_act:
            cola.append(cmds.pop(0))
        if cola:
            ratios_resp = [(tiempo_act - tiempo_lleg + tiempo_raf) / tiempo_raf for _, tiempo_lleg, tiempo_raf in cola]
            idx = ratios_resp.index(max(ratios_resp))
            cmd, tiempo_lleg, tiempo_raf = cola.pop(idx)
            hilo = threading.Thread(target=ejecutar_comando, args=(imgs[cmd]['image_id'], tiempo_raf))
            hilo.start()
            hilo.join(tiempo_raf)
            tiempo_fin = tiempo_act + tiempo_raf - tiempo_lleg
            tiempo_resp = tiempo_act - tiempo_lleg
            tiempos_fin.append(tiempo_fin)
            tiempos_resp.append(tiempo_resp)
            prom_fin += tiempo_fin
            prom_resp += tiempo_resp
            print(f"HRRN - Cmd: {cmd}, Tiempo Fin: {tiempo_fin}, Tiempo Resp: {tiempo_resp}")
            tiempo_act += tiempo_raf
        else:
            tiempo_act += 1
    prom_fin = round(prom_fin / len(cmds_copia), 3)
    prom_resp = round(prom_resp / len(cmds_copia), 3)

    print(f"Promedio de tiempo de finalización: {prom_fin}")
    print(f"Promedio de tiempo de respuesta: {prom_resp}")

    return responses(tiempos_fin, tiempos_resp, prom_fin, prom_resp)

# Algoritmo Round Robin
def round_robin(cmds, imgs, quantum):
    tiempo_act = 0
    cola = []
    tiempos_fin = []
    tiempos_resp = []
    prom_fin = 0
    prom_resp = 0
    cmds_copia = cmds.copy()
    tiempos_raf = {i: tiempo_raf for i, (_, _, tiempo_raf) in enumerate(cmds)}
    while cmds or cola:
        while cmds and cmds[0][1] <= tiempo_act:
            cola.append(cmds.pop(0))
        if cola:
            cmd, tiempo_lleg, tiempo_raf = cola.pop(0)
            idx = list(tiempos_raf.keys())[list(tiempos_raf.values()).index(tiempo_raf)]
            if tiempo_raf > quantum:
                hilo = threading.Thread(target=ejecutar_comando, args=(imgs[cmd]['image_id'], quantum))
                hilo.start()
                hilo.join(quantum)
                tiempo_restante = tiempo_raf - quantum
                cola.append((cmd, tiempo_lleg, tiempo_restante))
                tiempos_raf[idx] -= quantum
                if idx not in tiempos_resp:
                    tiempos_resp[idx] = tiempo_act - tiempo_lleg
                tiempo_act += quantum
            else:
                hilo = threading.Thread(target=ejecutar_comando, args=(imgs[cmd][0], tiempo_raf))
                hilo.start()
                hilo.join(tiempo_raf)
                tiempo_fin = tiempo_act + tiempo_raf - tiempo_lleg
                tiempo_resp = tiempos_resp.get(idx, tiempo_act - tiempo_lleg)
                tiempos_fin.append(tiempo_fin)
                tiempos_resp.append(tiempo_resp)
                prom_fin += tiempo_fin
                prom_resp += tiempo_resp
                print(f"Round Robin - Cmd: {cmd}, Tiempo Fin: {tiempo_fin}, Tiempo Resp: {tiempo_resp}")
                tiempo_act += tiempo_raf
        else:
            tiempo_act += 1
    prom_fin = round(prom_fin / len(cmds_copia), 3)
    prom_resp = round(prom_resp / len(cmds_copia), 3)

    print(f"Promedio de tiempo de finalización: {prom_fin}")
    print(f"Promedio de tiempo de respuesta: {prom_resp}")

    return responses(tiempos_fin, tiempos_resp, prom_fin, prom_resp)
