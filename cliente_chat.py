
import socket
import threading

HOST = "127.0.0.1"
PUERTO = 5000

cliente = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

cliente.connect((HOST, PUERTO))

nombre = input("Escribe tu nombre: ")

cliente.sendall(
    (nombre + "\n").encode("utf-8")
)


def recibir_mensajes():

    archivo = cliente.makefile(
        "r",
        encoding="utf-8",
        newline="\n"
    )

    try:
        while True:

            mensaje = archivo.readline()

            if not mensaje:
                break

            print("\n" + mensaje.rstrip("\r\n"))

    except OSError:
        pass

    finally:
        archivo.close()


# Crear hilo para recibir mensajes
hilo = threading.Thread(
    target=recibir_mensajes,
    daemon=True
)

hilo.start()

print("\nComandos disponibles:")
print("/usuarios = ver usuarios conectados")
print("/salir = desconectarse")

while True:

    mensaje = input("")

    cliente.sendall(
        (mensaje + "\n").encode("utf-8")
    )

    if mensaje == "/salir":
        break

cliente.close()
