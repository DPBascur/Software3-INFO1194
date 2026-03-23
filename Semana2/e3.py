#implementa un programa con 10 hilos, donde cada hilo intenta acceder a un recurso
#compartido. Usa un semaforo para permitir que solo 3 hilos puedan acceder simultaneamente al recurso compartido. Cada hilo debe imprimir un mensaje cuando accede al recurso y otro mensaje cuando lo libera.
#a ese recurso

import threading
import time


HILOS = 10
MAX_DENTRO = 3

semaforo = threading.Semaphore(MAX_DENTRO)


def usar_recurso(i: int) -> None:
	# El semáforo limita cuántos hilos pueden estar “dentro” al mismo tiempo.
	with semaforo:
		print(f"Hilo {i} ACCEDE al recurso")
		time.sleep(0.5)  # simula trabajo usando el recurso compartido
		print(f"Hilo {i} LIBERA el recurso")


def main() -> None:
	hilos = [threading.Thread(target=usar_recurso, args=(i,)) for i in range(1, HILOS + 1)]

	for h in hilos:
		h.start()
	for h in hilos:
		h.join()


if __name__ == "__main__":
	main()