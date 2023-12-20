def tiene_alguna_mayuscula(text: str) -> bool:
    return any(list(map(str.isupper, text)))


def verificar_largo(minimo, maximo, texto):
    return minimo <= len(texto) <= maximo


def tiene_algun_numero(text: str) -> bool:
    return any(list(map(lambda x: x in "0123456789", text)))


def obtener_pos_conejo(laberinto: list) -> tuple:
    for x, fila in enumerate(laberinto):
        for y, _ in enumerate(fila):
            if laberinto[x][y] == "C":
                return x, y
