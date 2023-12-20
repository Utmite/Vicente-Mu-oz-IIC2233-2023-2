import typing
from PyQt6 import QtCore
from PyQt6.QtWidgets import (
    QWidget,
    QMainWindow,
    QVBoxLayout,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction
from frontend.components.components import Mensaje, Botones
from frontend.components.sonido import SonidoGanar, SonidoPerder


class FinJuego(QMainWindow):
    evento_cerrar_aplicacion: pyqtSignal = pyqtSignal()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.layout = QVBoxLayout()
        self.widget_principal = QWidget()
        self.widget_principal.setLayout(self.layout)

        self.resultado = Mensaje("", 20)
        self.botones = Botones(
            [
                ("Salir", self.evento_cerrar_aplicacion.emit),
            ]
        )

        self.layout.addWidget(self.resultado)
        self.layout.addWidget(self.botones)

        self.setCentralWidget(self.widget_principal)

        salir = QAction("salir", self)
        salir.setShortcut(Qt.Key.Key_Escape)
        salir.triggered.connect(self.evento_cerrar_aplicacion.emit)
        self.addAction(salir)

    def mostrar(self, resultado: str, puntaje: float):
        if ":c" in resultado:
            self.sonido = SonidoPerder()
        else:
            self.sonido = SonidoGanar()

        self.layout.addWidget(Mensaje(f"Puntaje Obtenido: {puntaje}"))
        self.resultado.message_label.setText(resultado)
        self.showMaximized()

    def mostar_desconeccion(self, resultado: str):
        self.sonido = SonidoPerder()

        self.layout.addWidget(Mensaje(f"Se ha perdido la conexión con el servidor F"))
        self.resultado.message_label.setText("")
        self.showMaximized()
