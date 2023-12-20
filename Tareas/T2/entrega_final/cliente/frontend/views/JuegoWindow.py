from PyQt6.QtWidgets import (
    QWidget,
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction
from frontend.components.juego import Juego
from frontend.components.informacion import Informacion


class JuegoWindow(QMainWindow):
    cerrar_aplicacion: pyqtSignal = pyqtSignal()

    def __init__(self, nivel: int = 1):
        super().__init__()
        self.nivel = nivel
        self.init_gui()
        self.atajos_teclado()

    def init_gui(self):
        screen = self.screen()
        screen_geometry = screen.geometry()

        self.setGeometry(0, 0, screen_geometry.width(), screen_geometry.height())
        self.setMaximumSize(screen_geometry.width(), screen_geometry.height())

        self.informacion = Informacion()
        self.juego = Juego(self.nivel)

        # Poner vidas en el tablero de inicio
        self.informacion.poner_vidas(self.juego.mundo.conejo_chico.vidas)

        # Ir cambiando el tiempo en informacion
        self.juego.mundo.evento_cambio_nivel_duracion_y_puntaje.connect(
            self.informacion.poner_timepo_y_puntaje
        )

        # Poner vidas cuando cambia
        self.juego.mundo.evento_cambio_vidas_conejo_chico.connect(
            self.informacion.poner_vidas
        )

        # Obtuvo un itme
        self.juego.mundo.evento_actualizar_inventario.connect(
            self.informacion.poner_inventario
        )

        # Itenta usar un item
        self.juego.mundo.evento_poner_item.connect(
            self.informacion.inventario_clase.poner_item
        )

        # Apreto salir
        self.informacion.evento_cerrar_aplicacion.connect(self.cerrar_aplicacion)

        # Aprto pausa
        self.informacion.evento_pausar.connect(self.juego.mundo.alternar_pausa)

        # Poner item
        self.informacion.inventario_clase.evento_usar_item.connect(
            self.juego.mundo.usar_item
        )

        self.layout = QHBoxLayout()
        self.main = QWidget()
        self.layout.addWidget(self.informacion)

        self.juego_widget = QWidget()
        self.juego_layout = QVBoxLayout()
        self.juego_layout.addWidget(self.juego)
        self.setContentsMargins(0, 0, 0, 10)
        self.juego_widget.setLayout(self.juego_layout)

        self.layout.addWidget(self.juego_widget)
        self.main.setLayout(self.layout)
        self.setCentralWidget(self.main)

        style = "background-color: black;"
        self.setStyleSheet(style)

    def atajos_teclado(self):
        salir = QAction("salir", self)
        salir.setShortcut(Qt.Key.Key_Escape)
        salir.triggered.connect(self.cerrar_aplicacion.emit)
        self.addAction(salir)

    def cargar_partida_e_iniciar_juego(
        self, puede, respuesta, nombre, puntos: float, nivel, *args
    ):
        if puede:
            self.juego.mundo.nivel = nivel + 1
            self.juego.mundo.puntaje_original = puntos

            self.juego.mundo.conejo_chico.nombre = nombre
            self.juego.mundo.cargar_laberinto()
            self.juego.mundo.vida_conejo()

            self.show()

    def ocultar(self, *args):
        self.hide()
