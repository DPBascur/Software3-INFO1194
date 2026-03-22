import threading
import time
from statistics import mean
import matplotlib.pyplot as plt

LIMITE = 1_000_000
REPETICIONES = 5
CANTIDADES_HILOS = [1, 2, 4, 8, 16]


def dividir_rangos(inicio, fin, cantidad_hilos):
	total_numeros = fin - inicio + 1
	base = total_numeros // cantidad_hilos
	sobrantes = total_numeros % cantidad_hilos

	rangos = []
	actual = inicio

	for i in range(cantidad_hilos):
		tam = base + (1 if i < sobrantes else 0)
		sub_inicio = actual
		sub_fin = actual + tam - 1
		rangos.append((sub_inicio, sub_fin))
		actual = sub_fin + 1

	return rangos


def sumar_subrango(inicio, fin, resultados, indice):
	acumulado = 0
	for numero in range(inicio, fin + 1):
		acumulado += numero
	resultados[indice] = acumulado


def ejecutar_experimento(cantidad_hilos):
	tiempos = []
	esperado = (LIMITE * (LIMITE + 1)) // 2

	for _ in range(REPETICIONES):
		rangos = dividir_rangos(1, LIMITE, cantidad_hilos)
		resultados = [0] * cantidad_hilos
		hilos = []

		inicio_tiempo = time.perf_counter()

		for i, (inicio, fin) in enumerate(rangos):
			hilo = threading.Thread(target=sumar_subrango, args=(inicio, fin, resultados, i))
			hilos.append(hilo)
			hilo.start()

		for hilo in hilos:
			hilo.join()

		fin_tiempo = time.perf_counter()
		suma_total = sum(resultados)

		if suma_total != esperado:
			raise ValueError(
				f"Resultado inválido con {cantidad_hilos} hilos: {suma_total} != {esperado}"
			)

		tiempos.append(fin_tiempo - inicio_tiempo)

	return {
		"hilos": cantidad_hilos,
		"promedio": mean(tiempos),
		"minimo": min(tiempos),
		"maximo": max(tiempos),
		"tiempos": tiempos,
	}


def imprimir_tabla(resultados):
	print("\nResultados del experimento (segundos)")
	print("-" * 58)
	print(f"{'Hilos':<8}{'Promedio':<16}{'Mínimo':<16}{'Máximo':<16}")
	print("-" * 58)
	for r in resultados:
		print(f"{r['hilos']:<8}{r['promedio']:<16.6f}{r['minimo']:<16.6f}{r['maximo']:<16.6f}")
	print("-" * 58)


def graficar(resultados):
	x = [r["hilos"] for r in resultados]
	y_promedio = [r["promedio"] for r in resultados]
	y_min = [r["minimo"] for r in resultados]
	y_max = [r["maximo"] for r in resultados]

	plt.figure(figsize=(9, 5))
	plt.plot(x, y_promedio, marker="o", label="Promedio")
	plt.plot(x, y_min, marker="s", linestyle="--", label="Mínimo")
	plt.plot(x, y_max, marker="^", linestyle="--", label="Máximo")
	plt.title("Rendimiento por cantidad de hilos")
	plt.xlabel("Número de hilos")
	plt.ylabel("Tiempo total (segundos)")
	plt.xticks(x)
	plt.grid(True, alpha=0.3)
	plt.legend()
	plt.tight_layout()
	plt.savefig("t3_grafica.png", dpi=150)
	print("\nGráfica guardada en: t3_grafica.png")


def analizar(resultados):
	mejor = min(resultados, key=lambda x: x["promedio"])
	peor = max(resultados, key=lambda x: x["promedio"])

	print("\nAnálisis breve:")
	print(
		f"- Mejor promedio: {mejor['hilos']} hilo(s) con {mejor['promedio']:.6f} s."
	)
	print(
		f"- Peor promedio: {peor['hilos']} hilo(s) con {peor['promedio']:.6f} s."
	)
	print(
		"- En tareas de suma numérica (CPU-bound), aumentar hilos en Python no siempre mejora"
	)
	print(
		"  porque el GIL limita la ejecución paralela real de bytecode y además hay overhead"
	)
	print(
		"  de crear/sincronizar hilos. Por eso suele existir un punto donde más hilos deja de"
	)
	print("  ser conveniente o incluso empeora el tiempo.")


def main():
	resultados = []

	print("Iniciando experimento de rendimiento...")
	print(f"Rango evaluado: 1 a {LIMITE}")
	print(f"Repeticiones por configuración: {REPETICIONES}")

	for cantidad in CANTIDADES_HILOS:
		print(f"\nProbando con {cantidad} hilo(s)...")
		resultados.append(ejecutar_experimento(cantidad))

	imprimir_tabla(resultados)
	graficar(resultados)
	analizar(resultados)


if __name__ == "__main__":
	main()
