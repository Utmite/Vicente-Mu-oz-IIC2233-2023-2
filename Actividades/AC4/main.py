from typing import List
from clases import Tortuga
import pickle


###################
#### ENCRIPTAR ####
###################
def serializar_tortuga(tortuga: Tortuga) -> bytearray:
    try:
        return bytearray(pickle.dumps(tortuga))
    except AttributeError:
        raise ValueError()


def verificar_rango(mensaje: bytearray, inicio: int, fin: int) -> None:
    if inicio < 0 or fin > len(mensaje) or fin < inicio:
        raise AttributeError

    return None


def codificar_rango(inicio: int, fin: int) -> bytearray:
    binicio = bytearray(inicio.to_bytes(3, "big"))
    bfin = bytearray(fin.to_bytes(3, "big"))
    return binicio + bfin


def codificar_largo(largo: int) -> bytearray:
    # Completar
    return bytearray(largo.to_bytes(3, "big"))


def separar_msg(mensaje: bytearray, inicio: int, fin: int) -> List[bytearray]:
    m_extraido = mensaje[inicio : fin + 1]
    m_con_mascara = mensaje.copy()
    # Completar

    if len(m_extraido) % 2 == 1:
        m_extraido = m_extraido[::-1]

    i = 0
    for k, v in enumerate(m_con_mascara):
        if inicio <= k <= fin:
            m_con_mascara[k] = i
            i += 1

    return [m_extraido, m_con_mascara]


def encriptar(mensaje: bytearray, inicio: int, fin: int) -> bytearray:
    # Se la damos listas
    verificar_rango(mensaje, inicio, fin)

    m_extraido, m_con_mascara = separar_msg(mensaje, inicio, fin)
    rango_codificado = codificar_rango(inicio, fin)
    return (
        codificar_largo(fin - inicio + 1)
        + m_extraido
        + m_con_mascara
        + rango_codificado
    )


######################
#### DESENCRIPTAR ####
######################
def deserializar_tortuga(mensaje_codificado: bytearray) -> Tortuga:
    # Completar
    try:
        return pickle.loads(mensaje_codificado)
    except ValueError:
        raise AttributeError


def decodificar_largo(mensaje: bytearray) -> int:
    # Completar
    return int.from_bytes(mensaje[:3], byteorder="big")


def separar_msg_encriptado(mensaje: bytearray) -> List[bytearray]:
    m_extraido = bytearray()
    m_con_mascara = bytearray()
    rango_codificado = bytearray()
    # Completar

    largo = int.from_bytes(mensaje[:3], byteorder="big")
    mensaje_sin_largo = mensaje[3:]

    m_extraido = mensaje_sin_largo[:largo]
    m_con_mascara = mensaje_sin_largo[largo:-6]
    rango_codificado = mensaje_sin_largo[-6:]

    if len(m_extraido) % 2 == 1:
        m_extraido = m_extraido[::-1]

    return [m_extraido, m_con_mascara, rango_codificado]


def decodificar_rango(rango_codificado: bytearray) -> List[int]:
    inicio = rango_codificado[:3]
    fin = rango_codificado[3:]

    inicio = int.from_bytes(inicio, byteorder="big")
    fin = int.from_bytes(fin, byteorder="big")

    return [inicio, fin]


def desencriptar(mensaje: bytearray) -> bytearray:
    # Completar
    m_extraido, m_con_mascara, rango_codificado = separar_msg_encriptado(mensaje)
    inicio, fin = decodificar_rango(rango_codificado)

    i = 0
    for k, v in enumerate(m_con_mascara):
        if inicio <= k <= fin:
            m_con_mascara[k] = m_extraido[i]
            i += 1
    return m_con_mascara


if __name__ == "__main__":
    # Tortuga
    tama = Tortuga("Tama2")
    print("Nombre: ", tama.nombre)
    print("Edad: ", tama.edad)
    print(tama.celebrar_anivesario())
    print()

    # Encriptar
    original = serializar_tortuga(tama)
    print("Original: ", original)
    encriptado = encriptar(original, 6, 24)
    print("Encriptado: ", encriptado)
    print()

    # Desencriptar
    mensaje = bytearray(
        b"\x00\x00\x13roT\x07\x8c\x94sesalc\x06\x8c\x00\x00\x00\x00\x00\x80\x04\x958\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12tuga\x94\x93\x94)\x81\x94}\x94(\x8c\x06nombre\x94\x8c\x05Tama2\x94\x8c\x04edad\x94K\x01ub.\x00\x00\x06\x00\x00\x18"
    )
    desencriptado = desencriptar(mensaje)
    tama = deserializar_tortuga(desencriptado)

    # Tortuga
    print("Tortuga: ", tama)
    print("Nombre: ", tama.nombre)
    print("Edad: ", tama.edad)
