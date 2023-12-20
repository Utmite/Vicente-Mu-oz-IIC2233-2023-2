from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
)
from PyQt6.QtGui import QAction, QShortcut, QKeySequence
from PyQt6.QtCore import Qt, pyqtSignal
from frontend.components.components import Sprite
from typing import List
from backend.mundo.mundo import Mundo


class Juego(QWidget):
    def __init__(self, nivel: int):
        super().__init__()
        self.init_gui()

        self.nivel = nivel
        self.mundo = Mundo(nivel)

        self.mundo.evento_se_cargo_el_mundo.connect(self.pintar)
        self.atajos_teclado()

    def init_gui(self):
        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        self.grid.setVerticalSpacing(0)
        self.grid.setHorizontalSpacing(0)
        self.setLayout(self.grid)

    def atajos_teclado(self):
        bajar = QAction(self)
        bajar.setShortcut(Qt.Key.Key_S)
        bajar.triggered.connect(self.mundo.conejo_chico.direccion_S)

        self.addAction(bajar)

        subir = QAction(self)
        subir.setShortcut(Qt.Key.Key_W)
        subir.triggered.connect(self.mundo.conejo_chico.direccion_W)
        self.addAction(subir)

        derecha = QAction(self)
        derecha.setShortcut(Qt.Key.Key_D)
        derecha.triggered.connect(self.mundo.conejo_chico.direccion_D)
        self.addAction(derecha)

        izquierda = QAction(self)
        izquierda.setShortcut(Qt.Key.Key_A)
        izquierda.triggered.connect(self.mundo.conejo_chico.direccion_A)
        self.addAction(izquierda)

        recoger_item = QAction(self)
        recoger_item.setShortcut(Qt.Key.Key_G)
        recoger_item.triggered.connect(self.mundo.conejo_chico.recoger_item)
        self.addAction(recoger_item)

        pausa = QAction(self)
        pausa.setShortcut(Qt.Key.Key_P)
        pausa.triggered.connect(self.mundo.alternar_pausa)
        self.addAction(pausa)

        borrar_villanos = QAction(self)
        borrar_villanos.setShortcut(
            QKeySequence(Qt.Key.Key_K, Qt.Key.Key_I, Qt.Key.Key_L)
        )
        borrar_villanos.triggered.connect(self.mundo.borrar_villanos)
        self.addAction(borrar_villanos)

        infinito = QAction(self)
        infinito.setShortcut(QKeySequence(Qt.Key.Key_I, Qt.Key.Key_N, Qt.Key.Key_F))
        infinito.triggered.connect(self.mundo.infinito)
        self.addAction(infinito)

    def pintar(self, laberinto_sprites: List[List[Sprite]], *args) -> None:
        for fila, elementos in enumerate(laberinto_sprites):
            for columna, sprite in enumerate(elementos):
                self.grid.addWidget(sprite, fila, columna)

        for i in range(len(laberinto_sprites)):
            self.grid.setRowStretch(i, 1)
        for i in range(len(laberinto_sprites[0])):
            self.grid.setColumnStretch(i, 1)
