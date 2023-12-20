import json
from typing import Dict


def usuario_permitido(nombre: str, usuarios_no_permitidos: list[str]) -> bool:
    return nombre not in usuarios_no_permitidos


def serializar_mensaje(mensaje: str) -> bytearray:
    return bytearray(mensaje.encode(encoding="UTF-8"))


def separar_mensaje(mensaje: bytearray) -> list[bytearray]:
    a = bytearray()
    b = bytearray()
    c = bytearray()
    todas = [a, b, c]

    for i, byte in enumerate(mensaje):
        if i != 0 and i % 3 == 0:
            todas = todas[::-1]
        todas[i % 3].append(byte)

    return [a, b, c]


def encriptar_mensaje(mensaje: bytearray) -> bytearray:
    a, b, c = separar_mensaje(mensaje)
    condicion = a[0] + b[-1] + c[0]

    if condicion % 2 == 0:
        resultado = bytearray(b"1") + a + c + b
    else:
        resultado = bytearray(b"0") + b + a + c
    return resultado


def codificar_mensaje(mensaje: bytearray) -> list[bytearray]:
    largo = len(mensaje)
    largo = largo.to_bytes(4, "big")

    chunks = []
    resultado = []
    resultado.append(bytearray(largo))

    for i in range(0, len(mensaje), 36):
        chunk = mensaje[i : i + 36]

        while len(chunk) < 36:
            chunk.append(0)

        chunks.append(bytearray(chunk))

    for i, chunk in enumerate(chunks, 1):
        numero_bloque = i.to_bytes(4, "big")
        resultado.append(bytearray(numero_bloque))
        resultado.append(chunk)

    return resultado


def serializar_encriptar_codificar(mensaje_json: str) -> bytearray:
    return codificar_mensaje(encriptar_mensaje(serializar_mensaje(mensaje_json)))


def descodificar_mensaje(chunks: Dict[int, bytearray]) -> bytearray:
    ultimo_numero_chunk = max(chunks.keys())
    ultimo_datos_chunk = bytearray(chunks[ultimo_numero_chunk])

    # borrar los ultimos 0 que se agregaron para llegar a los 36 bytes
    while ultimo_datos_chunk[-1] == 0x00:
        ultimo_datos_chunk.pop()

    chunks[ultimo_numero_chunk] = ultimo_datos_chunk

    bytearray_datos = bytearray([byte for datos in chunks.values() for byte in datos])

    return bytearray_datos


def desencriptar_mensaje(bytes: bytearray) -> bytearray:
    tipo_encriptacion = bytes[0:1]
    bytearray_datos = bytes[1:]

    y1, y2, y3 = separar_mensaje([0] * len(bytearray_datos))
    y1, y2, y3 = len(y1), len(y2), len(y3)

    if tipo_encriptacion == b"1":
        a = bytearray_datos[:y1]
        c = bytearray_datos[y1 : y1 + y3]
        b = bytearray_datos[y1 + y3 :]
    elif tipo_encriptacion == b"0":
        b = bytearray_datos[:y2]
        a = bytearray_datos[y2 : y2 + y1]
        c = bytearray_datos[y2 + y1 :]

    mensaje_bytearray = bytearray()

    grupos = [a, b, c]

    for i in range(len(bytearray_datos)):
        if i != 0 and i % 3 == 0:
            grupos = grupos[::-1]
        if grupos[i % 3]:
            mensaje_bytearray.append(grupos[i % 3].pop(0))

    return mensaje_bytearray


def deserializar_mensaje(bytes: bytearray) -> str:
    return bytes.decode("utf-8")


def largo_a_chunks(largo):
    return len(range(0, largo, 36))


def log(quien: str, accion: str = "---", info: str = "---"):
    print(
        f"{quien:<20} | {accion:<30} | {f'{info}':<20}",
    )
    print("-" * 60)
