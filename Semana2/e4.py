#Simula un retaurante que solo puede atender un numero limitado de clientes al mismo tiempo.
#Usa un semaforo para controlar la capacidad del restaurante, y hacer que los demas clientes esperen
#hasta que haya espacio disponible.

import threading
import time


CAPACIDAD = 4   # máximo de clientes dentro del restaurante
CLIENTES = 12   # total de clientes que llegan

semaforo = threading.Semaphore(CAPACIDAD)


def cliente(i: int) -> None:
	print(f"Cliente {i} llega y espera mesa...")

	# Si no hay cupo (contador del semáforo en 0), este hilo se bloquea aquí.
	with semaforo:
		print(f"Cliente {i} ENTRA (hay cupo)")
		time.sleep(0.7)  # simulamos el tiempo de atención/comida
		print(f"Cliente {i} SALE (libera cupo)")


def main() -> None:
	hilos = [threading.Thread(target=cliente, args=(i,)) for i in range(1, CLIENTES + 1)]

	for h in hilos:
		h.start()
		time.sleep(0.1)  # llegan escalonados para que se note la espera

	for h in hilos:
		h.join()


if __name__ == "__main__":
	main()