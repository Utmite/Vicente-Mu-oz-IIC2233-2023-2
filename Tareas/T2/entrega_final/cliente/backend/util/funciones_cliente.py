from backend.util.util import (
    tiene_alguna_mayuscula,
    verificar_largo,
    tiene_algun_numero,
    obtener_pos_conejo,
)
from copy import deepcopy
from os import path
from typing import List
from parametros import (
    LARGO_LABERINTO,
    ANCHO_LABERINTO,
)


def validacion_formato(nombre: str) -> bool:
    return (
        nombre.isalnum()
        and tiene_alguna_mayuscula(nombre)
        and verificar_largo(3, 16, nombre)
        and tiene_algun_numero(nombre)
    )


def riesgo_mortal(laberinto: list[list]) -> bool:
    conejo_x, conejo_y = obtener_pos_conejo(laberinto)

    # fila hacia la derecha
    agregar = True
    fila_derecha = []
    for y in range(conejo_y + 1, len(laberinto[0])):
        if laberinto[conejo_x][y] == "P":
            agregar = False
        if agregar == True:
            fila_derecha.append(laberinto[conejo_x][y])

    fila_izquierda = []
    agregar = True
    for y in range(conejo_y - 1, -1, -1):
        if laberinto[conejo_x][y] == "P":
            agregar = False
        if agregar == True:
            fila_izquierda.append(laberinto[conejo_x][y])

    if any(list(map(lambda x: x in ["LH", "CL"], fila_derecha))):
        return True
    if any(list(map(lambda x: x in ["LH", "CR"], fila_izquierda))):
        return True

    agregar = True
    columan_abajo = []
    for x in range(conejo_x + 1, len(laberinto)):
        if laberinto[x][conejo_y] == "P":
            agregar = False
        if agregar == True:
            columan_abajo.append(laberinto[x][conejo_y])
    agregar = True
    columan_arriba = []
    for x in range(conejo_x - 1, -1, -1):
        if laberinto[x][conejo_y] == "P":
            agregar = False
        if agregar == True:
            columan_arriba.append(laberinto[x][conejo_y])

    if any(list(map(lambda x: x in ["LV", "CU"], columan_abajo))):
        return True
    if any(list(map(lambda x: x in ["LV", "CD"], columan_arriba))):
        return True

    return False


def usar_item(item: str, inventario: list) -> tuple[bool, list]:
    if not any(list(map(lambda x: x == item, inventario))):
        return (False, deepcopy(inventario))
    else:
        x = deepcopy(inventario)
        x.remove(item)
        return (True, x)


def calcular_puntaje(
    tiempo: int, vidas: int, cantidad_lobos: int, PUNTAJE_LOBO: int
) -> float:
    try:
        valor = (tiempo * vidas) / (cantidad_lobos * PUNTAJE_LOBO)
    except ZeroDivisionError:
        valor = 0.00

    return round(valor, 2)


def validar_direccion(laberinto: list[list], tecla: str) -> bool:
    conejo_x, conejo_y = obtener_pos_conejo(laberinto)

    if tecla == "A":
        conejo_y -= 1
    elif tecla == "S":
        conejo_x += 1
    elif tecla == "D":
        conejo_y += 1
    elif tecla == "W":
        conejo_x -= 1

    try:
        casilla = laberinto[conejo_x][conejo_y]
        return casilla != "P"
    except IndexError:
        return False


def obtener_laberinto_nivel(nivel):
    laberinto_path = path.join(
        path.dirname(path.abspath(__file__)),
        f"../../frontend/assets/laberintos/tablero_{nivel}.txt",
    )
    laberinto: List[List[str]] = []
    with open(laberinto_path) as archivo:
        for linea in archivo.readlines():
            if (n := linea.strip()) != "":
                fila = n.split(",")
                fila.remove("")
                laberinto.append(fila)
    return laberinto
