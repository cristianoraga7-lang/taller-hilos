
import threading
import time
import statistics

tiempos = {
    "A": 1,
    "B": 2,
    "C": 1.5
}


def leer_sensor(nombre, duracion, inicio):
    comienzo = time.perf_counter() - inicio

    print(f"Sensor {nombre} inicia: {comienzo:.2f} s")

    time.sleep(duracion)

    final = time.perf_counter() - inicio

    print(f"Sensor {nombre} termina: {final:.2f} s")


def secuencial():
    inicio = time.perf_counter()

    for nombre, duracion in tiempos.items():
        leer_sensor(nombre, duracion, inicio)

    return time.perf_counter() - inicio


def concurrente():
    inicio = time.perf_counter()
    hilos = []

    for nombre, duracion in tiempos.items():
        hilo = threading.Thread(
            target=leer_sensor,
            args=(nombre, duracion, inicio)
        )
        hilos.append(hilo)
        hilo.start()

    for hilo in hilos:
        hilo.join()

    return time.perf_counter() - inicio


def join_despues_de_start():
    inicio = time.perf_counter()

    for nombre, duracion in tiempos.items():
        hilo = threading.Thread(
            target=leer_sensor,
            args=(nombre, duracion, inicio)
        )

        hilo.start()
        hilo.join()

    return time.perf_counter() - inicio


def probar(funcion):
    resultados = []

    for i in range(3):
        print(f"\nPrueba {i + 1}")
        resultado = funcion()
        resultados.append(resultado)

    mediana = statistics.median(resultados)

    print("\nMediana:", round(mediana, 2), "segundos")


print("1. MODO SECUENCIAL")
probar(secuencial)

print("\n2. MODO CONCURRENTE")
probar(concurrente)

print("\n3. JOIN DESPUES DE CADA START")
probar(join_despues_de_start)
