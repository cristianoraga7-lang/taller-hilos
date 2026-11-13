
import socket
import threading

HOST = "127.0.0.1"
PUERTO = 5000

usuarios = {}
lock_usuarios = threading.Lock()


def enviar(conexion, mensaje):
    datos = usuarios.get(conexion)

    if datos is None:
        return

    nombre, lock_envio = datos

    try:
        with lock_envio:
            conexion.sendall((mensaje + "\n").encode("utf-8"))
    except OSError:
        pass


def enviar_todos(mensaje):
    with lock_usuarios:
        conexiones = list(usuarios.keys())

    for conexion in conexiones:
        enviar(conexion, mensaje)


def atender_cliente(conexion, direccion):

    archivo = conexion.makefile(
        "r",
        encoding="utf-8",
        newline="\n"
    )

    nombre = archivo.readline().strip()

    if not nombre:
        conexion.close()
        return

    # Registrar usuario y su candado de envío
    with lock_usuarios:
        usuarios[conexion] = (
            nombre,
            threading.Lock()
        )

    print(nombre, "se ha conectado")

    enviar_todos(nombre + " se ha conectado")

    try:
        while True:

            mensaje = archivo.readline()

            if not mensaje:
                break

            mensaje = mensaje.rstrip("\r\n")

            if mensaje == "/usuarios":

                # Copiar nombres dentro del Lock
                with lock_usuarios:
                    lista = sorted(
                        datos[0] for datos in usuarios.values()
                    )

                respuesta = (
                    "Usuarios conectados: " + ", ".join(lista)
                )

                # Enviar únicamente al usuario que lo solicitó
                enviar(conexion, respuesta)

            elif mensaje == "/salir":
                break

            else:
                enviar_todos(nombre + ": " + mensaje)

    except OSError:
        pass

    finally:

        with lock_usuarios:
            usuarios.pop(conexion, None)

        archivo.close()
        conexion.close()

        print(nombre, "se ha desconectado")

        enviar_todos(nombre + " se ha desconectado")


servidor = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

servidor.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_REUSEADDR,
    1
)

servidor.bind((HOST, PUERTO))
servidor.listen()

print("Servidor iniciado...")
print("Esperando usuarios...")

while True:

    conexion, direccion = servidor.accept()

    hilo = threading.Thread(
        target=atender_cliente,
        args=(conexion, direccion)
    )

    hilo.start()
