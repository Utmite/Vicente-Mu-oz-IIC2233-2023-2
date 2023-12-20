import json
import os
from os import path
from typing import List


class Usuario:
    def __init__(self, nombre: str, puntos: float, ultimo_nivel: int) -> None:
        self.nombre = nombre
        self.puntos = puntos
        self.ultimo_nivel = int(ultimo_nivel)

    def __str__(self) -> str:
        return f"Usuario({self.nombre},{self.puntos},{self.ultimo_nivel})"

    def __repr__(self) -> str:
        return f"{self.nombre},{self.puntos},{self.ultimo_nivel}"

    def __eq__(self, otro) -> bool:
        if not isinstance(otro, Usuario):
            return False
        return self.nombre == otro.nombre

    def json(self):
        return json.dumps(self.__dict__)


class Datos:
    def __init__(self) -> None:
        self.data_path = path.join(path.dirname(path.abspath(__file__)), "puntaje.txt")
        if not os.path.exists(self.data_path):
            with open(self.data_path, "w", encoding="utf-8") as archivo:
                pass

        with open(self.data_path, "r", encoding="utf-8") as archivo:
            lineas: List[str] = archivo.readlines()

        self.usuarios: List[str] = list(
            map(
                lambda x: [item.strip() for item in x.split(",") if item.strip() != ""],
                lineas,
            )
        )

        self.usuarios: List[Usuario] = list(
            map(lambda x: Usuario(x[0], x[1], x[2]), self.usuarios)
        )

    def obtener_salon_de_la_fama(self):
        self.usuarios = sorted(
            self.usuarios, key=lambda x: float(x.puntos), reverse=True
        )
        return self.usuarios[:5]

    def guardar_usuario(self, usuario: Usuario):
        if usuario in self.usuarios:
            self.usuarios.remove(usuario)

        self.usuarios.append(usuario)
        usuarios: List[str] = list(map(lambda x: repr(x) + "\n", self.usuarios))

        with open(self.data_path, "w", encoding="utf-8") as archivo:
            archivo.writelines(usuarios)
