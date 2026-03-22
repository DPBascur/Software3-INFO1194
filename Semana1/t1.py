import threading
from time import sleep, time
import random as ra

resultados = [None, None, None, None]

def tarea(id_hilo):
    tiempo_inicio = time()

    for i in range(5):
        sleep(ra.uniform(0.2, 0.8))
        print(f"Hola Mundo desde el hilo {id_hilo}, iteración {i+1}")

    tiempo_final = time()
    tiempo_total = tiempo_final - tiempo_inicio
    resultados[id_hilo - 1] = (f"Hilo-{id_hilo}", 5, tiempo_total)


# Creación de los 4 hilos
hilo1 = threading.Thread(target=tarea, args=(1,), name="Hilo-1")
hilo2 = threading.Thread(target=tarea, args=(2,), name="Hilo-2")
hilo3 = threading.Thread(target=tarea, args=(3,), name="Hilo-3")
hilo4 = threading.Thread(target=tarea, args=(4,), name="Hilo-4")

# Inicio de los hilos
hilo1.start()
hilo2.start()
hilo3.start()
hilo4.start()

# Finalización de los hilos
hilo1.join()
hilo2.join()
hilo3.join()
hilo4.join()

print("\nResumen final:")
for nombre, mensajes, tiempo in resultados:
    print(f"{nombre} -> mensajes: {mensajes}, tiempo: {tiempo:.2f} segundos")
