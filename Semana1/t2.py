"""t2.py — Suma de 1..LIMITE usando N hilos.

Se solicita al usuario un número N (cantidad de hilos). Luego se divide el rango
1..LIMITE en N subrangos contiguos (lo más equilibrados posible), se crea un hilo
por subrango y cada hilo calcula su suma parcial. Al final se agregan las sumas
parciales y se valida contra la fórmula cerrada:

    suma(1..L) = L*(L+1)/2

Notas importantes (contexto educativo):
- En CPython, los hilos no suelen acelerar trabajo CPU-bound por el GIL, pero
  este ejercicio sirve para practicar creación, sincronización (join) y reparto
  de trabajo.
- El límite de hilos se restringe a LIMITE para evitar casos absurdos (por
  ejemplo, más hilos que números a sumar).

Ejecución:
    python Semana1/t2.py
"""

import threading

# ======================
# Constantes de programa
# ======================

LIMITE = 1_000_000


# =====================
# Funciones auxiliares
# =====================


def dividir_rangos(inicio, fin, cantidad_hilos):
	"""Divide un rango entero inclusivo en subrangos contiguos.

	Los subrangos se reparten de forma lo más uniforme posible: si el total de
	números no es divisible por la cantidad de hilos, los primeros subrangos
	reciben 1 elemento extra.

	Args:
		inicio: Inicio del rango (inclusivo).
		fin: Fin del rango (inclusivo).
		cantidad_hilos: Cantidad de subrangos a generar (N > 0).

	Returns:
		Lista de tuplas (sub_inicio, sub_fin), ambas inclusivas.
	"""
	total_numeros = fin - inicio + 1
	tam_base = total_numeros // cantidad_hilos
	sobrantes = total_numeros % cantidad_hilos

	rangos = []
	actual = inicio

	for i in range(cantidad_hilos):
		tam = tam_base + (1 if i < sobrantes else 0)
		sub_inicio = actual
		sub_fin = actual + tam - 1
		rangos.append((sub_inicio, sub_fin))
		actual = sub_fin + 1

	return rangos


# =====================
# Trabajo de cada hilo
# =====================


def sumar_subrango(indice, inicio, fin, resultados):
	"""Calcula la suma de un subrango y guarda el resultado en una lista compartida.

	Este patrón evita bloqueos: cada hilo escribe en una posición única
	(`resultados[indice]`), por lo que no hay escrituras concurrentes al mismo
	objeto.

	Args:
		indice: Índice del hilo (0..N-1), usado para posicionar el resultado.
		inicio: Inicio del subrango (inclusivo).
		fin: Fin del subrango (inclusivo).
		resultados: Lista compartida de tamaño N donde se almacenan diccionarios con
			la información calculada por cada hilo.
	"""
	suma_parcial = 0
	for numero in range(inicio, fin + 1):
		suma_parcial += numero

	resultados[indice] = {
		"hilo": f"Hilo-{indice + 1}",
		"rango": (inicio, fin),
		"suma": suma_parcial,
	}


# ==================
# Programa principal
# ==================


def main():
	"""Punto de entrada interactivo.

	Flujo:
	1) Pide N al usuario.
	2) Valida que N sea entero positivo y razonable.
	3) Divide el rango 1..LIMITE en N subrangos.
	4) Lanza N hilos, espera con join y agrega resultados.
	5) Valida contra la suma esperada por fórmula.
	"""
	entrada = input("Ingrese la cantidad de hilos (N): ").strip()

	if not entrada.isdigit() or int(entrada) <= 0:
		print("N debe ser un entero positivo.")
		return

	n_hilos = int(entrada)
	if n_hilos > LIMITE:
		print(f"N no puede ser mayor a {LIMITE} para este problema.")
		return

	rangos = dividir_rangos(1, LIMITE, n_hilos)
	resultados = [None] * n_hilos
	hilos = []

	for i, (inicio, fin) in enumerate(rangos):
		hilo = threading.Thread(target=sumar_subrango, args=(i, inicio, fin, resultados))
		hilos.append(hilo)
		hilo.start()

	for hilo in hilos:
		hilo.join()

	suma_total_hilos = 0
	print("\nAporte de cada hilo:")
	for resultado in resultados:
		inicio, fin = resultado["rango"]
		suma_parcial = resultado["suma"]
		suma_total_hilos += suma_parcial
		print(f"{resultado['hilo']} -> rango [{inicio}, {fin}] suma = {suma_parcial}")

	esperado = (LIMITE * (LIMITE + 1)) // 2

	print("\nResumen:")
	print(f"Suma total por hilos: {suma_total_hilos}")
	print(f"Suma esperada       : {esperado}")

	if suma_total_hilos == esperado:
		print("Validación: CORRECTA")
	else:
		print("Validación: INCORRECTA")


if __name__ == "__main__":
	main()
