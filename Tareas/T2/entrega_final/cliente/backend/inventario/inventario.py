from PyQt6.QtCore import QObject, pyqtSignal
from frontend.components.components import ItemInventario, Sprite


class Inventario(QObject):
    evento_usar_item = pyqtSignal(object, object)
    evento_madar_mensaje_item = pyqtSignal(str)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.item_seleccionado = None

    def seleccionar_item(self, item: ItemInventario):
        self.item_seleccionado = item

    def poner_item(self, casilla: Sprite):
        if self.item_seleccionado == None:
            self.evento_madar_mensaje_item.emit("Ningun item seleccionado")
            return
        if casilla.fondo == "P" or len(casilla.entidades) > 0:
            self.evento_madar_mensaje_item.emit("Casilla invalida")
            return
        self.evento_madar_mensaje_item.emit("")
        self.evento_usar_item.emit(self.item_seleccionado, casilla)
        self.item_seleccionado = None
