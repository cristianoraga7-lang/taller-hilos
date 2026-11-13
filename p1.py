
import threading

inventario = 1
ventas = []

barrera = threading.Barrier(2)


def vender_sin_lock(nombre):
    global inventario

    # Consultar inventario
    hay_producto = inventario > 0

    print(nombre, "consultó:", inventario)

    # Esperar a que ambas cajas consulten
    barrera.wait()

    # Realizar la venta
    if hay_producto:
        inventario -= 1
        ventas.append(nombre)
        print(nombre, "vendió el producto")
    else:
        print(nombre, "no pudo vender")


hilo1 = threading.Thread(
    target=vender_sin_lock,
    args=("Caja 1",)
)

hilo2 = threading.Thread(
    target=vender_sin_lock,
    args=("Caja 2",)
)

hilo1.start()
hilo2.start()

hilo1.join()
hilo2.join()

print("\nVentas aprobadas:", len(ventas))
print("Inventario final:", inventario)
