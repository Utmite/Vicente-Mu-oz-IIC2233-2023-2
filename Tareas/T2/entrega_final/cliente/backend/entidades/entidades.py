from PyQt6.QtCore import QObject, pyqtSignal, QTimer, QMutex
from typing import List


class Entidad(QObject):
    evento_cambio_vida: pyqtSignal = pyqtSignal(int, int, object)
    evento_entidad_se_movio = pyqtSignal(int, int, int, int, object)
    entidad_id = 0

    def __init__(
        self, fila: int, col: int, nombre_sprite: str, vidas: int = 1, **kwargs
    ) -> None:
        super().__init__(**kwargs)

        self.fila: int = fila
        self.col: int = col
        self.nombre_sprite = nombre_sprite
        self.id = Entidad.entidad_id
        self._vidas = vidas
        self.inmortalidad = False
        Entidad.entidad_id += 1

    @property
    def vidas(self):
        return self._vidas

    @vidas.setter
    def vidas(self, vidas: int):
        aux = self.vidas
        if not self.inmortalidad:
            self._vidas = vidas if vidas >= 0 else 0
        self.evento_cambio_vida.emit(aux, self.vidas, self)

    def interactuar(self, entidad) -> None:
        pass

    def __eq__(self, otro) -> bool:
        if not isinstance(otro, Entidad):
            return False
        otro: Entidad
        return self.id == otro.id

    def cambiar_mortalidad(self, valor: bool):
        self.inmortalidad = valor


class EntidadMovimiento(Entidad):
    def __init__(self, mutex: QMutex, velocidad: float, **kwargs) -> None:
        super().__init__(**kwargs)

        self.velocidad = round((1 / velocidad) * 1000)
        self.velocidad_original = self.velocidad
        self.direccion = ""

        self.bucle_velocidad = QTimer()
        self.bucle_velocidad.setInterval(self.velocidad)
        self.bucle_velocidad.timeout.connect(self.movimiento)
        self.bucle_velocidad.start()

        self.paso_animacion = 0
        self.animacion_actual = ""
        self.animaciones = {}
        self.mutex = mutex

    def animacion(self, paso_animacion: int | None = None):
        if paso_animacion != None:
            self.paso_animacion = paso_animacion

        if (n := self.animaciones.get(self.animacion_actual)) is None:
            return
        self.paso_animacion = (
            self.paso_animacion + 1 if self.paso_animacion + 1 < len(n) else 0
        )
        self.nombre_sprite = n[self.paso_animacion]

    def movimiento(self):
        self.mutex.lock()
        if self.direccion in ["W", "CU"]:
            self.subir()
        elif self.direccion in ["S", "CD"]:
            self.bajar()
        elif self.direccion in ["D", "CR"]:
            self.derecha()
        elif self.direccion in ["A", "CL"]:
            self.izquierda()

        self.mutex.unlock()

    def subir(self):
        self.evento_entidad_se_movio.emit(
            self.fila, self.col, self.fila - 1, self.col, self
        )

    def bajar(self):
        self.evento_entidad_se_movio.emit(
            self.fila, self.col, self.fila + 1, self.col, self
        )

    def derecha(self):
        self.evento_entidad_se_movio.emit(
            self.fila, self.col, self.fila, self.col + 1, self
        )

    def izquierda(self):
        self.evento_entidad_se_movio.emit(
            self.fila, self.col, self.fila, self.col - 1, self
        )

    def cambiar_velocidad(self, velocidad):
        self.velocidad = round((1 / velocidad) * 1000)
        self.bucle_velocidad.setInterval(self.velocidad)

    def ponderar_velociad(self, ponderacion: int = 1):
        self.velocidad = round(self.velocidad * ponderacion)
        self.bucle_velocidad.setInterval(self.velocidad)

    def recuperar_velociad_original(self):
        self.velocidad = self.velocidad_original
        self.bucle_velocidad.setInterval(self.velocidad)


class ConejoChico(EntidadMovimiento):
    evento_recoger_item: pyqtSignal = pyqtSignal(object)

    def __init__(self, nombre="", **kwargs) -> None:
        super().__init__(nombre_sprite="conejo.png", **kwargs)
        self.cantidad_lobos_eliminados = 0
        self.animaciones = {
            "W": [
                "conejo_arriba_1.png",
                "conejo_arriba_2.png",
                "conejo_arriba_3.png",
            ],
            "D": [
                "conejo_derecha_1.png",
                "conejo_derecha_2.png",
                "conejo_derecha_3.png",
            ],
            "A": [
                "conejo_izquierda_1.png",
                "conejo_izquierda_2.png",
                "conejo_izquierda_3.png",
            ],
            "S": [
                "conejo_abajo_1.png",
                "conejo_abajo_2.png",
                "conejo_abajo_3.png",
            ],
        }
        self.inventario: List[Item] = []
        self.nombre = nombre

    def direccion_W(self):
        self.direccion = "W"
        self.animacion_actual = "W"

    def direccion_S(self):
        self.direccion = "S"
        self.animacion_actual = "S"

    def direccion_A(self):
        self.direccion = "A"
        self.animacion_actual = "A"

    def direccion_D(self):
        self.direccion = "D"
        self.animacion_actual = "D"

    def recoger_item(self):
        self.evento_recoger_item.emit(self)

    def interactuar(self, entidad) -> bool:
        if isinstance(entidad, (Lobo, Zanahoria)):
            self.vidas -= 1


class Lobo(EntidadMovimiento):
    def interactuar(self, entidad) -> bool:
        if isinstance(entidad, ConejoChico):
            entidad.vidas -= 1

        if isinstance(entidad, Explosion):
            self.vidas = 0
        if isinstance(entidad, Congelacion):
            self.ponderar_velociad(1.25)


class LovoHorizontal(Lobo):
    def __init__(self, **kwargs) -> None:
        super().__init__(nombre_sprite="lobo_horizontal_izquierda_1.png", **kwargs)

        self.animaciones = {
            "A": [
                "lobo_horizontal_izquierda_1.png",
                "lobo_horizontal_izquierda_2.png",
                "lobo_horizontal_izquierda_3.png",
            ],
            "D": [
                "lobo_horizontal_derecha_1.png",
                "lobo_horizontal_derecha_2.png",
                "lobo_horizontal_derecha_3.png",
            ],
        }

        self.direccion_A()

    def direccion_A(self):
        self.direccion = "A"
        self.animacion_actual = "A"

    def direccion_D(self):
        self.direccion = "D"
        self.animacion_actual = "D"


class LovoVertical(Lobo):
    def __init__(self, **kwargs) -> None:
        super().__init__(nombre_sprite="lobo_vertical_abajo_1.png", **kwargs)

        self.animaciones = {
            "S": [
                "lobo_vertical_abajo_1.png",
                "lobo_vertical_abajo_2.png",
                "lobo_vertical_abajo_3.png",
            ],
            "W": [
                "lobo_vertical_arriba_1.png",
                "lobo_vertical_arriba_2.png",
                "lobo_vertical_arriba_3.png",
            ],
        }

        self.direccion_S()

    def direccion_W(self):
        self.direccion = "W"
        self.animacion_actual = "W"

    def direccion_S(self):
        self.direccion = "S"
        self.animacion_actual = "S"


class Zanahoria(EntidadMovimiento):
    def __init__(self, direccion: str, **kwargs) -> None:
        super().__init__(nombre_sprite="", **kwargs)

        if direccion == "CU":
            self.nombre_sprite = "zanahoria_arriba.png"
        elif direccion == "CD":
            self.nombre_sprite = "zanahoria_abajo.png"
        elif direccion == "CL":
            self.nombre_sprite = "zanahoria_izquierda.png"
        elif direccion == "CR":
            self.nombre_sprite = "zanahoria_derecha.png"
        else:
            raise ValueError("Esa direccion no existe")

        self.direccion = direccion

    def interactuar(self, entidad) -> bool:
        if isinstance(entidad, ConejoChico):
            entidad.vidas -= 1

    def __str__(self) -> str:
        return f"Zanahoria({self.direccion})"


class Canon(Entidad):
    evento_disparar: pyqtSignal = pyqtSignal(int, int, Entidad)

    def __init__(self, orientacion: str, intervalo_disparo: int, **kwargs) -> None:
        super().__init__(nombre_sprite="", **kwargs)

        if orientacion == "CU":
            self.nombre_sprite = "canon_arriba.png"
        elif orientacion == "CD":
            self.nombre_sprite = "canon_abajo.png"
        elif orientacion == "CL":
            self.nombre_sprite = "canon_izquierda.png"
        elif orientacion == "CR":
            self.nombre_sprite = "canon_derecha.png"
        else:
            raise ValueError(f"Esa orientacion no existe: {orientacion}")
        self.orientacion = orientacion
        self.bucle_disparo = QTimer()
        self.bucle_disparo.setInterval(int(intervalo_disparo * 1000))
        self.bucle_disparo.timeout.connect(self.disparar)
        self.bucle_disparo.start()

    def disparar(self):
        if self.orientacion == "CU":
            self.subir()
        elif self.orientacion == "CD":
            self.bajar()
        elif self.orientacion == "CR":
            self.derecha()
        elif self.orientacion == "CL":
            self.izquierda()

    def cambiar_intervalo_disparo(self, intervalo_disparo: int):
        self.bucle_disparo.setInterval(int(intervalo_disparo * 1000))

    def subir(self):
        self.evento_disparar.emit(self.fila - 1, self.col, self)

    def bajar(self):
        self.evento_disparar.emit(self.fila + 1, self.col, self)

    def derecha(self):
        self.evento_disparar.emit(self.fila, self.col + 1, self)

    def izquierda(self):
        self.evento_disparar.emit(self.fila, self.col - 1, self)


class Item(Entidad):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def __str__(self) -> str:
        return f"Item({self.nombre_sprite.replace('.png', '')})"

    def __repr__(self) -> str:
        return f"Item({self.nombre_sprite.replace('.png', '')})"


class BombaManzana(Item):
    def __init__(self, **kwargs) -> None:
        super().__init__(nombre_sprite="manzana_burbuja.png", **kwargs)


class BombaCongelacion(Item):
    def __init__(self, **kwargs) -> None:
        super().__init__(nombre_sprite="congelacion_burbuja.png", **kwargs)


class Efectos(Entidad):
    def __init__(self, tiempo_bomba: int, **kwargs) -> None:
        super().__init__(**kwargs)

        self.tiempo_bomba = tiempo_bomba
        self.bucle_duracion = QTimer()
        self.bucle_duracion.singleShot(int(tiempo_bomba * 1000), self.desaparecer)

    def desaparecer(self):
        self.vidas = 0

    def __str__(self) -> str:
        return f"Efecto({self.nombre_sprite})"


class Explosion(Efectos):
    def __init__(self, **kwargs) -> None:
        super().__init__(nombre_sprite="explosion.png", **kwargs)


class Congelacion(Efectos):
    def __init__(self, **kwargs) -> None:
        super().__init__(nombre_sprite="congelacion.png", **kwargs)
