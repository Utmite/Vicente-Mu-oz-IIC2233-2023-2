from PyQt6.QtWidgets import (
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QAction
from frontend.components.components import (
    DCCLogo,
    Mensaje,
    Botones,
    EntradaTexto,
)


class MainWindow(QMainWindow):
    cerrar_aplicacion = pyqtSignal()
    apreta_ingresar = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ejemplo de PyQt6 MainWindow")
        self.setStyleSheet("background-color: #FFB6C1;")
        self.setGeometry(0, 0, 1080, 720)
        self.showMaximized()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout()

        w = QWidget()
        self.layout3 = QVBoxLayout()

        self.layout3.addWidget(DCCLogo())
        self.layout3.addWidget(Mensaje("¿UNA PARTIDA?"))
        self.entradaNombre = EntradaTexto("Ingresa tu nickname")
        self.layout3.addWidget(self.entradaNombre)

        botones = Botones(
            [
                ("Ingresar", self.apreto_ingresar),
                ("Salir", self.cerrar_aplicacion.emit),
            ]
        )

        z = QWidget()
        self.layout5 = QVBoxLayout()
        self.mensaje_ingreser = Mensaje("", 20)
        self.layout5.addWidget(botones)
        self.layout5.addWidget(self.mensaje_ingreser)

        z.setLayout(self.layout5)

        self.layout3.addWidget(z)
        w.setLayout(self.layout3)
        self.layout.addWidget(w)

        self.fama_widget = QWidget()
        self.fama_widget.setStyleSheet(
            "border: 2px solid purple; background-color: pink; font-size: 15px; color: #9370DB; font-weight: bold;"
        )
        self.layout.addWidget(self.fama_widget)

        central_widget.setLayout(self.layout)

        ingresar = QAction("ingresar", self)
        ingresar.setShortcut(Qt.Key.Key_Return)
        ingresar.triggered.connect(self.apreto_ingresar)
        self.addAction(ingresar)

        salir = QAction("salir", self)
        salir.setShortcut(Qt.Key.Key_Escape)
        salir.triggered.connect(self.cerrar_aplicacion.emit)
        self.addAction(salir)

    def iniciar_juego(self, puede: bool, mensaje: str, *args) -> None:
        self.mensaje_ingreser.message_label.setText(mensaje)

        if puede == True:
            self.hide()

    def mostrar_salon_de_la_fama(self, mensaje: list):
        layout = QVBoxLayout()

        for k, v in enumerate(mensaje, 1):
            nombre = v["nombre"]
            puntos = v["puntos"]

            label = QLabel(f"{k}. {nombre} | puntos: {puntos}")
            layout.addWidget(label)

        self.fama_widget.setLayout(layout)

    def apreto_ingresar(self):
        y = self.entradaNombre.entrada.text()
        self.apreta_ingresar.emit(y)

    def ocultar(self, *args):
        self.hide()
