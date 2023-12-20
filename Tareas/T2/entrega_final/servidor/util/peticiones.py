import json
from threading import Thread, Event, Lock
from socket import socket
from util.funciones_servidor import (
    descodificar_mensaje,
    desencriptar_mensaje,
    deserializar_mensaje,
    largo_a_chunks,
    codificar_mensaje,
    encriptar_mensaje,
    serializar_mensaje,
    usuario_permitido,
    log,
)
from typing import Dict, List
from util.datos_guardados import Datos, Usuario


class JugadorOnline(Thread):
    guardar: Lock = Lock()
    datos: Datos = Datos()

    def __init__(self, cliente: socket, address: str, nombres_baneados: list):
        super().__init__()
        self._cliente = cliente
        self._address = address
        self._desconectar = Event()
        self.nombre = None
        self.nombres_baneados = nombres_baneados
        self._cliente.settimeout(3)

    def run(self):
        try:
            while not self._desconectar.is_set():
                try:
                    data = self._cliente.recv(4)
                except TimeoutError:
                    log(str(self.nombre), "No se recivio mensaje")
                    continue
                if not data:
                    self.desconectar()
                    break

                largo = int.from_bytes(data, byteorder="big")

                mensaje = self._recivir_mensaje(largo)

                self.verificar_nombre(mensaje)
                self.pedir_salon_de_la_fama(mensaje)
                self.guardar_usuario(mensaje)

        except ConnectionError:
            self._cliente.close()
            log(str(self.nombre), "desconectar")
        except OSError:
            log(str(self.nombre), "desconectar")

    def desconectar(self):
        self._desconectar.set()
        self._cliente.close()

    def _recivir_mensaje(self, largo) -> dict:
        chunks: Dict[int, bytearray] = {}
        largo = largo_a_chunks(largo)

        if largo == 0:
            return

        while len(chunks.keys()) < largo:
            datos = self._cliente.recv(40)

            numero_chunk = int.from_bytes(datos[:4], "big")
            datos_chunl = datos[4:]

            chunks[numero_chunk] = datos_chunl

        bytes = descodificar_mensaje(chunks)
        bytes = desencriptar_mensaje(bytes)
        mensaje = deserializar_mensaje(bytes)

        mensaje = json.loads(mensaje)

        return mensaje

    def mandar_mensaje_json(self, mensaje):
        if not isinstance(mensaje, dict):
            raise ValueError("No es un dic")

        mensaje = json.dumps(mensaje)

        bytes_mensaje = serializar_mensaje(mensaje)
        bytes_mensaje = encriptar_mensaje(bytes_mensaje)
        chunks = codificar_mensaje(bytes_mensaje)

        bytearray_datos = bytearray([dato for i in chunks for dato in i])
        self._cliente.sendall(bytearray_datos)

    def pedir_salon_de_la_fama(self, mensaje):
        if (n := mensaje.get("pedir_salon_de_la_fama")) is not None and n == True:
            salon_de_la_fama = JugadorOnline.datos.obtener_salon_de_la_fama()
            salon_de_la_fama = list(map(lambda x: x.json(), salon_de_la_fama))
            while len(salon_de_la_fama) < 5:
                salon_de_la_fama.append(
                    json.dumps({"nombre": "--Desconocido--", "puntos": 0})
                )

            self.mandar_mensaje_json({"salon_de_la_fama": salon_de_la_fama})

            log(str(self.nombre), "obtener salon de la fama")

    def verificar_nombre(self, mensaje):
        if (nombre := mensaje.get("nombre")) is not None:
            puede = usuario_permitido(nombre, self.nombres_baneados)

            usuario: List[Usuario] = list(
                filter(lambda x: x.nombre == nombre, JugadorOnline.datos.usuarios)
            )

            usuario: Usuario = usuario[0] if len(usuario) > 0 else Usuario(nombre, 0, 0)

            respuesta = {
                "permitido_jugar": puede,
                "nombre": usuario.nombre,
                "puntos": usuario.puntos,
                "nivel": usuario.ultimo_nivel,
            }
            self.mandar_mensaje_json(respuesta)
            self.nombre = nombre

            log(str(self.nombre), "verificacion", f"Baneado: {not puede}")

    def guardar_usuario(self, mensaje):
        with JugadorOnline.guardar:
            if (nombre := mensaje.get("guardar_usuario")) is None:
                return
            JugadorOnline.datos.guardar_usuario(
                Usuario(self.nombre, mensaje["puntaje"], mensaje["nivel"])
            )

            log(str(self.nombre), "guardar", f"Datos de {str(self.nombre)}")
