#Implementa dos funciones sobre un contador compartido: una lo incrementa y 
#otra lo decrementa 1000 cada una, Para eviddenciar mejor la condicion de carrera realiza la oracion en pasos
#separados (leer eln contador, modificar una var temporal, esperar un instante y escribir el nuevo valor) luego
#usan un lock para proteger esa seccion critica

import threading
import time
import random as ra


N = 1000          # cada función hace 1000 operaciones
INTENTOS = 20     # repetimos para que sea fácil ver el error sin lock
ESPERA = 0.00001  # pausa mínima para “forzar” el entrelazado entre hilos
ESPERA2= ra.randint(1, 10) * 0.00001  # pausa aleatoria para aumentar la probabilidad de errores sin lock   
contador = 0
lock = threading.Lock()


def cambiar(delta: int, usar_lock: bool) -> None:
	"""Suma `delta` al contador N veces.

	La operación se hace en pasos separados para evidenciar la condición de carrera:
	leer -> modificar temporal -> esperar -> escribir.
	"""
	global contador

	for _ in range(N):
		if usar_lock:
			with lock:
				tmp = contador
				tmp = tmp + delta
				time.sleep(ESPERA)
				contador = tmp
		else:
			tmp = contador
			tmp = tmp + delta
			time.sleep(ESPERA2)
			contador = tmp


def incrementar(usar_lock: bool) -> None:
	cambiar(+1, usar_lock)


def decrementar(usar_lock: bool) -> None:
	cambiar(-1, usar_lock)


def ejecutar(usar_lock: bool) -> int:
	global contador
	contador = 0

	t1 = threading.Thread(target=incrementar, args=(usar_lock,))
	t2 = threading.Thread(target=decrementar, args=(usar_lock,))
	t1.start()
	t2.start()
	t1.join()
	t2.join()

	return contador


def main() -> None:
	# Sin lock: idealmente debería dar 0, pero a veces da != 0 por condición de carrera
	errores = 0
	ejemplo = None
	for _ in range(INTENTOS):
		res = ejecutar(usar_lock=False)
		if res != 0:
			errores += 1
			if ejemplo is None:
				ejemplo = res

	print(f"Sin lock: {errores}/{INTENTOS} resultados != 0" + (f" (ejemplo: {ejemplo})" if ejemplo is not None else ""))

	# Con lock: la sección crítica es atómica, por lo tanto el resultado debe ser 0
	print("Con lock:", ejecutar(usar_lock=True))


if __name__ == "__main__":
	main()