from copy import copy
from collections import defaultdict
from functools import reduce
from itertools import product
from typing import Generator

from parametros import RUTA_PELICULAS, RUTA_GENEROS
from utilidades import (
    Pelicula,
    Genero,
    obtener_unicos,
    imprimir_peliculas,
    imprimir_generos,
    imprimir_peliculas_genero,
)


# ----------------------------------------------------------------------------
# Parte 1: Cargar dataset
# ----------------------------------------------------------------------------


def cargar_peliculas(ruta: str) -> Generator:
    with open(ruta, "r") as archivo:
        lineas = archivo.readlines()
        for i in range(1, len(lineas)):
            texto = lineas[i].strip().split(",")
            yield Pelicula(
                int(texto[0]), texto[1], texto[2], int(texto[3]), float(texto[4])
            )


def cargar_generos(ruta: str) -> Generator:
    with open(ruta, "r") as archivo:
        lineas = archivo.readlines()
        for i in range(1, len(lineas)):
            texto = lineas[i].strip().split(",")
            yield Genero(texto[0], int(texto[1]))


# ----------------------------------------------------------------------------
# Parte 2: Consultas sobre generadores
# ----------------------------------------------------------------------------


def obtener_directores(generador_peliculas: Generator) -> set:
    x = map(lambda i: i.director, generador_peliculas)
    unicos = obtener_unicos(x)

    return unicos


def obtener_str_titulos(generador_peliculas: Generator) -> str:
    titulos = str(reduce(lambda x, y: x + y.titulo + ", ", generador_peliculas, ""))
    return titulos[:-2]


def filtro(e, director, rating_min, rating_max):
    salida = True
    if director != None:
        if e.director != director:
            salida = False
    if rating_min != None:
        if e.rating < rating_min:
            salida = False
    if rating_max != None:
        if e.rating > rating_max:
            salida = False
    return salida


def filtrar_peliculas(
    generador_peliculas: Generator,
    director: str | None = None,
    rating_min: float | None = None,
    rating_max: float | None = None,
) -> filter:
    # TODO: Completar

    x = filter(
        lambda e: filtro(e, director, rating_min, rating_max), generador_peliculas
    )
    return x


def filtrar_peliculas_por_genero(
    generador_peliculas: Generator,
    generador_generos: Generator,
    genero: str | None = None,
) -> Generator:
    r = product(generador_peliculas, generador_generos)
    r = filter(lambda x: x[0].id_pelicula == x[1].id_pelicula, r)

    if genero:
        r = filter(lambda x: x[1].genero == genero, r)

    return r


# ----------------------------------------------------------------------------
# Parte 3: Iterables
# ----------------------------------------------------------------------------


class DCCMax:
    def __init__(self, peliculas: list) -> None:
        self.peliculas = peliculas

    def __iter__(self):
        # TODO: Completar
        return IteradorDCCMax(self.peliculas)


class IteradorDCCMax:
    def __init__(self, iterable_peliculas: list) -> None:
        peliculas = copy(iterable_peliculas)
        self.peliculas = list(
            sorted(peliculas, key=lambda i: (i.estreno, -i.rating), reverse=True)
        )

    def __iter__(self):
        # TODO: Completar
        return self

    def __next__(self) -> tuple:
        if len(self.peliculas) == 0:
            raise StopIteration()
        return self.peliculas.pop()


if __name__ == "__main__":
    print("> Cargar películas:")
    imprimir_peliculas(cargar_peliculas(RUTA_PELICULAS))
    print()

    print("> Cargar géneros")
    imprimir_generos(cargar_generos(RUTA_GENEROS), 5)
    print()

    print("> Obtener directores:")
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    print(list(obtener_directores(generador_peliculas)))
    print()

    print("> Obtener string títulos")
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    print(obtener_str_titulos(generador_peliculas))
    print()

    print("> Filtrar películas (por director):")
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    imprimir_peliculas(
        filtrar_peliculas(generador_peliculas, director="Christopher Nolan")
    )
    print("\n> Filtrar películas (rating min):")
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    imprimir_peliculas(filtrar_peliculas(generador_peliculas, rating_min=9.1))
    print("\n> Filtrar películas (rating max):")
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    imprimir_peliculas(filtrar_peliculas(generador_peliculas, rating_max=8.7))
    print()

    print("> Filtrar películas por género")
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    generador_generos = cargar_generos(RUTA_GENEROS)
    imprimir_peliculas_genero(
        filtrar_peliculas_por_genero(
            generador_peliculas, generador_generos, "Biography"
        )
    )
    print()

    print("> DCC Max")
    for estreno, pelis in DCCMax(list(cargar_peliculas(RUTA_PELICULAS))):
        print(f"\n{estreno:^80}\n")
        imprimir_peliculas(pelis)
