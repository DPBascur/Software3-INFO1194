import threading

LIMITE = 1_000_000


def dividir_rangos(inicio, fin, cantidad_hilos):
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


def sumar_subrango(indice, inicio, fin, resultados):
	suma_parcial = 0
	for numero in range(inicio, fin + 1):
		suma_parcial += numero

	resultados[indice] = {
		"hilo": f"Hilo-{indice + 1}",
		"rango": (inicio, fin),
		"suma": suma_parcial,
	}


def main():
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
