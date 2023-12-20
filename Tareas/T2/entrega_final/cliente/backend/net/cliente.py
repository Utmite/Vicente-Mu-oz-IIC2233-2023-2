import socket
import json

from PyQt6.QtCore import QThread, pyqtSignal, QTimer
from backend.net.funciones_servidor import (
    descodificar_mensaje,
    desencriptar_mensaje,
    deserializar_mensaje,
    largo_a_chunks,
    codificar_mensaje,
    encriptar_mensaje,
    serializar_mensaje,
)
from typing import Dict


class Cliente(QThread):
    se_recivio_mensaje = pyqtSignal(dict)
    evento_se_desconecto = pyqtSignal(str)

    def __init__(self, host: str, port: int) -> None:
        super().__init__()
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._host = host
        self._port = port
        self._sock.connect((self._host, self._port))
        self.bucle_comprobar_coneccion = QTimer()
        self.bucle_comprobar_coneccion.setInterval(1000)
        self.bucle_comprobar_coneccion.timeout.connect(self.comprobar_coneccion)

    def run(self):
        self.bucle_comprobar_coneccion.start()
        while True:
            data = self._sock.recv(4)
            if not data:
                self.evento_se_desconecto.emit("El servidor se ha desconectado :c")
                self._sock.close()
                break

            largo = int.from_bytes(data, byteorder="big")
            mensaje = self._recivir_mensaje(largo)
            self.se_recivio_mensaje.emit(mensaje)

    def _recivir_mensaje(self, largo) -> dict:
        chunks: Dict[int, bytearray] = {}
        largo = largo_a_chunks(largo)

        if largo == 0:
            return

        while len(chunks.keys()) < largo:
            datos = self._sock.recv(40)

            numero_chunk = int.from_bytes(datos[:4], "big")
            datos_chunl = datos[4:]

            chunks[numero_chunk] = datos_chunl

        bytes = descodificar_mensaje(chunks)

        bytes = desencriptar_mensaje(bytes)
        mensaje = deserializar_mensaje(bytes)

        mensaje = json.loads(mensaje)

        return mensaje

    def mandar_mensaje_json(self, mensaje: dict):
        if not isinstance(mensaje, dict):
            raise ValueError("No es un dic")

        mensaje = json.dumps(mensaje)

        bytes_mensaje = serializar_mensaje(mensaje)
        bytes_mensaje = encriptar_mensaje(bytes_mensaje)
        chunks = codificar_mensaje(bytes_mensaje)

        bytearray_datos = bytearray([dato for i in chunks for dato in i])
        self._sock.sendall(bytearray_datos)

    def comprobar_coneccion(self):
        print("holaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        self.mandar_mensaje_json(mensaje={"ping": "ping"})
