import sys
import json
import socket
from util.peticiones import JugadorOnline
from typing import List
from os import path
from util.funciones_servidor import log


def main():
    args = sys.argv
    if len(args) <= 1:
        log(
            "Tienes que ingresar argumentos al llamar la funcion: 'python3 main.py <port>'"
        )
        return

    configuracion_path = path.join(
        path.dirname(path.abspath(__file__)), "configuracion.json"
    )
    with open(configuracion_path, "r", encoding="utf-8") as archivo:
        contenido: dict = json.load(archivo)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = contenido["host"]
    puerto = int(args[1])
    nombres_baneados = contenido.get("nombres_baneados", [])

    sock.bind((host, puerto))
    sock.listen()

    log("Servidor", "Iniciado", f"Host: {host}, Port: {puerto}")

    log("Servidor", "Cargando nombres baneados", nombres_baneados[:3])

    lista_de_conecciones: List[JugadorOnline] = []
    try:
        while True:
            socket_cliente, address = sock.accept()

            x = JugadorOnline(
                socket_cliente,
                address,
                nombres_baneados=nombres_baneados,
            )

            x.start()
            lista_de_conecciones.append(x)
    except KeyboardInterrupt:
        for x in lista_de_conecciones:
            x.desconectar()

    log("Servidor", "Cerrando servidor", "Chao Chao ...")
    sock.close()


if __name__ == "__main__":
    main()
