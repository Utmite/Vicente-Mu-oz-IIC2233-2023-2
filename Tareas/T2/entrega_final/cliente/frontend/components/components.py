from PyQt6 import QtGui
from PyQt6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLineEdit,
)

from PyQt6.QtGui import QPixmap, QPainter
from os import path
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from typing import List, Tuple, Callable, Dict
from backend.entidades.entidades import Entidad


class DCCLogo(QWidget):
    def __init__(self):
        super().__init__()

        image_path = path.join(
            path.dirname(path.abspath(__file__)), "../assets/sprites/logo.png"
        )
        pixmap = QPixmap(image_path)

        self.imagen = QLabel()
        self.imagen.setPixmap(pixmap)

        layout = QVBoxLayout()
        layout.addWidget(self.imagen)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)


class Sprite(QLabel):
    evento_poner_item = pyqtSignal(object)
    codigo: int = 0

    def __init__(self, fondo, entidades: List[Entidad] = []):
        super().__init__()
        self.codigo = Sprite.codigo
        Sprite.codigo += 1
        self.fondo: str = fondo
        self._entidades: List[Entidad] = entidades
        self.atrabesable = True

        self.pintar()

    @property
    def entidades(self):
        return self._entidades

    @entidades.setter
    def entidades(self, entidades: List[Entidad]):
        self._entidades = entidades
        self.pintar()

    def borrar_entidad(self, entidad: Entidad):
        if entidad not in self._entidades:
            return
        self._entidades.remove(entidad)
        self.pintar()

    def agregar_entidad(self, entidad: Entidad):
        if entidad in self._entidades:
            return
        self._entidades.append(entidad)
        self.pintar()

    def pintar(self):
        imagenes: List[QPixmap] = []

        if self.fondo != "P":
            image_path = path.join(
                path.dirname(path.abspath(__file__)),
                f"../assets/sprites/bloque_fondo.jpeg",
            )
            imagen = QPixmap(image_path)
            imagenes.append(imagen)
        else:
            image_path = path.join(
                path.dirname(path.abspath(__file__)),
                f"../assets/sprites/bloque_pared.jpeg",
            )
            imagen = QPixmap(image_path)
            imagenes.append(imagen)

        for entidad in self.entidades:
            image_path = path.join(
                path.dirname(path.abspath(__file__)),
                f"../assets/sprites/{entidad.nombre_sprite}",
            )
            if entidad.nombre_sprite in [
                "canon_abajo.png",
                "canon_arriba.png",
                "canon_derecha.png",
                "canon_izquierda.png",
            ]:
                self.atrabesable = False
            imagen = QPixmap(image_path)
            imagenes.append(imagen)

        combinado = QPixmap(QSize(40, 40))
        combinado.fill(Qt.GlobalColor.transparent)

        fondo = QPainter(combinado)

        for imagen in imagenes:
            imagen = imagen.scaled(40, 40)
            fondo.drawPixmap(0, 0, imagen)
        fondo.end()

        self.setPixmap(combinado)
        self.setScaledContents(True)

    def __repr__(self) -> str:
        return f"Sprite(entidades={self._entidades})"

    def __str__(self) -> str:
        return f"Sprite(entidades={self._entidades})"

    def __eq__(self, otro) -> bool:
        if not isinstance(otro, Sprite):
            return False
        otro: Sprite
        return self.codigo == otro.codigo

    def mousePressEvent(self, ev) -> None:
        self.evento_poner_item.emit(self)


class ItemInventario(QLabel):
    evento_seleccionar_item = pyqtSignal(object)
    codigo: int = 0

    def __init__(self, fondo: str):
        super().__init__()
        self.codigo = ItemInventario.codigo
        ItemInventario.codigo += 1
        self.fondo: str = ""

        if fondo == "manzana_burbuja.png":
            self.fondo = "manzana.png"
        elif fondo == "congelacion_burbuja.png":
            self.fondo = "congelacion.png"

        image_path = path.join(
            path.dirname(path.abspath(__file__)),
            f"../assets/sprites/{self.fondo}",
        )
        imagen = QPixmap(image_path)
        imagen = imagen.scaled(60, 60)
        self.setPixmap(imagen)

    def mousePressEvent(self, ev) -> None:
        self.evento_seleccionar_item.emit(self)

    def __eq__(self, otro) -> bool:
        if not isinstance(otro, ItemInventario):
            return False
        otro: ItemInventario
        return self.codigo == otro.codigo


class Mensaje(QWidget):
    def __init__(self, message, tamano_letra: int = 48):
        super().__init__()

        self.message_label = QLabel(message)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        estilo = f"font-size: {tamano_letra}px; color: #9370DB; font-weight: bold;"
        self.message_label.setStyleSheet(estilo)
        layout = QVBoxLayout()

        layout.addWidget(self.message_label)

        self.setLayout(layout)


class Botones(QWidget):
    def __init__(self, botones: List[Tuple[str, Callable]]):
        super().__init__()

        layout = QHBoxLayout()

        self.botones: Dict[str, QPushButton] = {}

        for texto, funcion in botones:
            boton = QPushButton(texto)
            boton.setStyleSheet("border-radius: 15px;")
            estilo = "font-size: 24px; background-color: #9370DB; color: white; font-weight: bold;"

            boton.setStyleSheet(estilo)
            if funcion is not None:
                boton.clicked.connect(funcion)

            self.botones[texto] = boton
            layout.addWidget(boton)

        self.setLayout(layout)


class EntradaTexto(QWidget):
    def __init__(self, texto):
        super().__init__()

        self.entrada = QLineEdit()
        self.entrada.setPlaceholderText(texto)

        estilo = "font-size: 20px; background-color: #ffc0cb; color: #9370DB; font-weight: semi-bold;"
        self.entrada.setStyleSheet(estilo)
        layout = QVBoxLayout()
        layout.addWidget(self.entrada)

        self.setLayout(layout)
