# Sincronización (Mutex)
# Simula transferencias entre 2 cuentas compartidas.
# Usa un Lock para que la transferencia sea atómica y no haya condición de carrera.

import threading


HILOS = 6
ITER = 200
MONTO = 5

# Saldos compartidos (dos cuentas): [A, B]
saldos = [1000, 1000]
lock = threading.Lock()


def transferir(origen: int, destino: int, monto: int) -> None:
    """Mueve dinero de `origen` a `destino` protegido por Lock."""
    global saldos

    with lock:
        if saldos[origen] >= monto:
            saldos[origen] -= monto
            saldos[destino] += monto


def worker() -> None:
    for _ in range(ITER):
        # Muchos hilos hacen transferencias al mismo tiempo.
        transferir(0, 1, MONTO)
        transferir(1, 0, MONTO)


def main() -> None:
    total_inicial = sum(saldos)
    print("Inicial:", saldos, "Total=", total_inicial)

    threads = [threading.Thread(target=worker) for _ in range(HILOS)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("Final:", saldos, "Total=", sum(saldos))


if __name__ == "__main__":
    main()

