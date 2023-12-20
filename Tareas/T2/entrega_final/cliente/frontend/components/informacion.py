from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout
from PyQt6.QtCore import pyqtSignal
from typing import List
from frontend.components.components import Mensaje, Botones, ItemInventario
from backend.inventario.inventario import Inventario


class Informacion(QWidget):
    evento_cerrar_aplicacion = pyqtSignal()
    evento_pausar = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.inventario_clase = Inventario()
        self.inventario_clase.evento_madar_mensaje_item.connect(self.poner_mensaje_item)
        self.layout = QVBoxLayout()

        self.tiempo = Mensaje("Tiempo restante: MM:SS", 20)
        self.vidas = Mensaje("Vidas restantes: --", 20)
        self.puntaje = Mensaje("Tu puntaje es: 0", 20)
        self.nivel = Mensaje("Nivel: --", 20)

        self.botones = Botones(
            [
                ("Pausa", self.evento_pausar.emit),
                ("Salir", self.evento_cerrar_aplicacion.emit),
            ]
        )

        self.titulo_inventario = Mensaje("Inventario", 36)
        self.inventario = QWidget()
        layout = QGridLayout()
        self.mensaje_item = Mensaje("", 24)

        self.inventario.setLayout(layout)

        layout_info = QVBoxLayout()
        self.info_general = QWidget()
        self.info_general.setLayout(layout_info)

        layout_info.addWidget(self.tiempo)
        layout_info.addWidget(self.vidas)
        layout_info.addWidget(self.puntaje)
        layout_info.addWidget(self.nivel)

        self.layout.addWidget(self.info_general)
        self.layout.addWidget(self.botones)
        self.layout.addWidget(self.mensaje_item)
        self.layout.addWidget(self.titulo_inventario)
        self.layout.addWidget(self.inventario)

        self.setLayout(self.layout)

    def poner_timepo_y_puntaje(self, nivel: int, segundos: int, puntaje: float):
        minutos = segundos // 60
        segundos = segundos % 60

        self.tiempo.message_label.setText(
            f"Tiempo restante: {minutos:02}:{segundos:02}"
        )
        self.puntaje.message_label.setText(f"Tu puntaje es: {puntaje}")
        self.nivel.message_label.setText(f"Nivel: {nivel}")

    def poner_vidas(self, vidas: int):
        self.vidas.message_label.setText(f"Vidas restantes: {vidas}")

    def poner_inventario(self, inventario: List[ItemInventario]):
        l = self.inventario.layout()
        for i in reversed(range(l.count())):
            l.itemAt(i).widget().setParent(None)
        for k, item in enumerate(inventario):
            item.evento_seleccionar_item.connect(self.inventario_clase.seleccionar_item)
            l.addWidget(item, k // 3, k % 3)

    def poner_mensaje_item(self, mensaje):
        self.mensaje_item.message_label.setText(mensaje)
