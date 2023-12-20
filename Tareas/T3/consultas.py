import collections
import itertools
import math
from datetime import datetime
from typing import Generator
from utilidades import Funciones


def peliculas_genero(generador_peliculas: Generator, genero: str):
    return (pelicula for pelicula in generador_peliculas if pelicula.genero == genero)


def personas_mayores(generador_personas: Generator, edad: int):
    return (persona for persona in generador_personas if persona.edad >= edad)


def funciones_fecha(generador_funciones: Generator, fecha: str):
    return (
        funcion
        for funcion in generador_funciones
        if datetime.strptime(funcion.fecha, "%d-%m-%y")
        == datetime.strptime(fecha, "%d-%m-%Y")
    )


def titulo_mas_largo(generador_peliculas: Generator) -> str:
    peliculas = [i for i in generador_peliculas]

    longitud_maxima = max(map(lambda x: len(x.titulo), peliculas), default=0)

    u = itertools.tee(filter(lambda x: len(x.titulo) == longitud_maxima, peliculas))

    z0 = next(u[1])
    z1 = next(u[1], None)
    if z1 is None:
        return z0.titulo

    u = itertools.tee(u[0])

    rating_maximo = max(map(lambda x: x.rating, u[1]), default=0)

    u = itertools.tee(u[0])

    u = itertools.tee(filter(lambda x: x.rating == rating_maximo, u[1]))

    z0 = next(u[1])
    z1 = next(u[1], None)
    if z1 is None:
        return z0.titulo

    z0 = max(u[0], key=lambda x: peliculas.index(x))

    return z0.titulo


def saber_anio(fecha):
    if 24 > int(fecha) > 0:
        return "20"
    return "19"


def normalizar_fechas(generador_funciones: Generator):
    return (
        Funciones(
            i.id,
            i.numero_sala,
            i.id_pelicula,
            i.horario,
            datetime.strptime(i.fecha, "%d-%m-%y").strftime("%Y-%m-%d")
            if datetime.strptime(i.fecha, "%d-%m-%y").year <= 2023
            else datetime.strptime(i.fecha, "%d-%m-%y")
            .replace(year=datetime.strptime(i.fecha, "%d-%m-%y").year - 100)
            .strftime("%Y-%m-%d"),
        )
        for i in generador_funciones
    )


def personas_reservas(generador_reservas: Generator):
    return {i.id_persona for i in generador_reservas}


def peliculas_en_base_al_rating(
    generador_peliculas: Generator, genero: str, rating_min: int, rating_max: int
):
    return (
        i
        for i in generador_peliculas
        if i.genero == genero and rating_min <= i.rating <= rating_max
    )


def mejores_peliculas(generador_peliculas: Generator):
    peliculas = [i for i in generador_peliculas]

    peliculas.sort(key=lambda i: i.rating, reverse=True)

    grouped_por_rating = itertools.groupby(
        peliculas, key=lambda pelicula: pelicula.rating
    )

    primeros_20_grupos = itertools.islice(grouped_por_rating, 20)

    def order_mismo_rating_por_id(i):
        x = [e for e in i]
        x.sort(key=lambda pelicula: pelicula.id)
        return x

    peliculas = [k for i in primeros_20_grupos for k in order_mismo_rating_por_id(i[1])]
    return (i for i in peliculas[:20])


def pelicula_genero_mayor_rating(generador_peliculas: Generator, genero: str) -> str:
    peliculas = [i for i in generador_peliculas if i.genero == genero]

    peliculas.sort(key=lambda i: i.rating, reverse=True)

    u = itertools.tee(filter(lambda i: i.rating == peliculas[0].rating, peliculas))

    z0 = next(u[1], "")
    z1 = next(u[1], None)

    if z0 == "":
        return z0
    elif z1 is None:
        return z0.titulo

    z0 = min(u[0], key=lambda x: peliculas.index(x))
    return z0.titulo


def fechas_funciones_pelicula(
    generador_peliculas: Generator, generador_funciones: Generator, titulo: str
):
    pelicula = next((i for i in generador_peliculas if i.titulo == titulo), None)
    return (
        i.fecha
        for i in generador_funciones
        if pelicula is not None and i.id_pelicula == pelicula.id
    )


def genero_mas_transmitido(
    generador_peliculas: Generator, generador_funciones: Generator, fecha: str
) -> str:
    try:
        funciones = [
            i.id_pelicula
            for i in generador_funciones
            if datetime.strptime(i.fecha, "%d-%m-%y")
            == datetime.strptime(fecha, "%d-%m-%Y")
        ]
    except ValueError:
        return ""

    genero = [i.genero for i in generador_peliculas if i.id in funciones]
    mas_transmitido = collections.Counter(genero).most_common(1)
    return "" if len(mas_transmitido) == 0 else mas_transmitido[0][0]


def id_funciones_genero(
    generador_peliculas: Generator, generador_funciones: Generator, genero: str
):
    peliculas = [i.id for i in generador_peliculas if i.genero == genero]

    return (i.id for i in generador_funciones if i.id_pelicula in peliculas)


def butacas_por_funcion(
    generador_reservas: Generator, generador_funciones: Generator, id_funcion: int
) -> int:
    funcion = next((i for i in generador_funciones if i.id == id_funcion), None)
    reservas = [
        i
        for i in generador_reservas
        if funcion.id is not None and i.id_funcion == funcion.id
    ]

    return len(reservas)


def salas_de_pelicula(
    generador_peliculas: Generator, generador_funciones: Generator, nombre_pelicula: str
):
    peliculas = [i.id for i in generador_peliculas if i.titulo == nombre_pelicula]

    return (i.numero_sala for i in generador_funciones if i.id_pelicula in peliculas)


def nombres_butacas_altas(
    generador_personas: Generator,
    generador_peliculas: Generator,
    generador_reservas: Generator,
    generador_funciones: Generator,
    titulo: str,
    horario: int,
):
    peliculas = [i.id for i in generador_peliculas if i.titulo == titulo]
    funcion = [
        i.id
        for i in generador_funciones
        if i.id_pelicula in peliculas and i.horario == horario
    ]
    reservas = [i.id_persona for i in generador_reservas if i.id_funcion in funcion]

    return (i.nombre for i in generador_personas if i.id in reservas)


def nombres_persona_genero_mayores(
    generador_personas: Generator,
    generador_peliculas: Generator,
    generador_reservas: Generator,
    generador_funciones: Generator,
    nombre_pelicula: str,
    genero: str,
    edad: int,
):
    peliculas = [i.id for i in generador_peliculas if i.titulo == nombre_pelicula]
    funcion = [i.id for i in generador_funciones if i.id_pelicula in peliculas]
    reservas = [i.id_persona for i in generador_reservas if i.id_funcion in funcion]

    return {
        i.nombre
        for i in generador_personas
        if i.id in reservas and i.genero == genero and i.edad >= edad
    }


def genero_comun(
    generador_personas: Generator,
    generador_peliculas: Generator,
    generador_reservas: Generator,
    generador_funciones: Generator,
    id_funcion: int,
) -> str:
    funcion = next((i for i in generador_funciones if i.id == id_funcion))
    pelicula = next((i for i in generador_peliculas if i.id == funcion.id_pelicula))
    reservas = [i.id_persona for i in generador_reservas if i.id_funcion == funcion.id]
    generos = [i.genero for i in generador_personas if i.id in reservas]

    contador = collections.Counter(generos)
    frecuencia_maxima = contador.most_common(1)[0][1]

    generos = [i[0] for i in contador.most_common() if i[1] == frecuencia_maxima]

    if len(generos) == 1:
        return f"En la función {id_funcion} de la película {pelicula.titulo} la mayor parte del público es {generos[0]}."

    elif len(generos) == 2:
        return f"En la función {id_funcion} de la película {pelicula.titulo} se obtiene que la mayor parte del público es de {generos[0]} y {generos[1]} con la misma cantidad de personas."
    else:
        return f"En la función {id_funcion} de la película {pelicula.titulo} se obtiene que la cantidad de personas es igual para todos los géneros."


def edad_promedio(
    generador_personas: Generator,
    generador_peliculas: Generator,
    generador_reservas: Generator,
    generador_funciones: Generator,
    id_funcion: int,
) -> str:
    funcion = next((i for i in generador_funciones if i.id == id_funcion))
    reservas = [i.id_persona for i in generador_reservas if i.id_funcion == funcion.id]

    pelicula = next((i for i in generador_peliculas if i.id == funcion.id_pelicula))
    edades = [i.edad for i in generador_personas if i.id in reservas]

    promedio = sum(edades) / len(edades)

    promedio = math.ceil(promedio)

    return f"En la función {id_funcion} de la película {pelicula.titulo} la edad promedio del público es {promedio}."


def obtener_horarios_disponibles(
    generador_peliculas: Generator,
    generador_reservas: Generator,
    generador_funciones: Generator,
    fecha_funcion: str,
    reservas_maximas: int,
):
    fecha_funcion = datetime.strptime(fecha_funcion, "%d-%m-%y")

    peliculas = [i for i in generador_peliculas]
    peliculas.sort(key=lambda i: i.rating, reverse=True)
    pelicula = peliculas[0]

    funciones = [
        i
        for i in generador_funciones
        if datetime.strptime(i.fecha, "%d-%m-%y") == fecha_funcion
        and i.id_pelicula == pelicula.id
    ]

    funciones_id = [i.id for i in funciones]

    reservas = [
        r.id_funcion for r in generador_reservas if r.id_funcion in funciones_id
    ]

    return {i.horario for i in funciones if reservas.count(i.id) < reservas_maximas}


def personas_no_asisten(
    generador_personas: Generator,
    generador_reservas: Generator,
    generador_funciones: Generator,
    fecha_inicio: str,
    fecha_termino: str,
):
    abajo = datetime.strptime(fecha_inicio, "%d-%m-%Y")
    arriba = datetime.strptime(fecha_termino, "%d-%m-%Y")

    funciones = [
        i.id
        for i in generador_funciones
        if abajo <= datetime.strptime(i.fecha, "%d-%m-%y") <= arriba
    ]

    reserva = [i.id_persona for i in generador_reservas if i.id_funcion in funciones]

    return (i for i in generador_personas if i.id not in reserva)
