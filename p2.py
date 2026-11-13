
import threading

inventario = 1
ventas = []

candado = threading.Lock()


def vender_con_lock(nombre):
    global inventario

    with candado:

        if inventario > 0:
            inventario -= 1
            ventas.append(nombre)

            print(nombre, "vendió el producto")

        else:
            print(nombre, "no pudo vender")


hilo1 = threading.Thread(
    target=vender_con_lock,
    args=("Caja 1",)
)

hilo2 = threading.Thread(
    target=vender_con_lock,
    args=("Caja 2",)
)

hilo1.start()
hilo2.start()

hilo1.join()
hilo2.join()

print("\nVentas aprobadas:", len(ventas))
print("Inventario final:", inventario)

# Comprobaciones
assert len(ventas) == 1
assert inventario == 0

print("Prueba superada correctamente")
