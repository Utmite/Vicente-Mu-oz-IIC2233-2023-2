from PyQt6.QtCore import QObject, pyqtSignal, QMutex, QTimer
from frontend.components.components import Sprite
from typing import Tuple, Dict, List
from parametros import (
    VELOCIDAD_CONEJO,
    CANTIDAD_VIDAS,
    VELOCIDAD_LOBO,
    VELOCIDAD_ZANAHORIA,
    INTERVALO_DISPARO_CANON,
    DURACION_NIVEL_INICIAL,
    PONDERADOR_LABERINTO_1,
    PONDERADOR_LABERINTO_2,
    PONDERADOR_LABERINTO_3,
    LARGO_LABERINTO,
    ANCHO_LABERINTO,
    TIEMPO_BOMBA,
    PUNTAJE_LOBO,
    PUNTAJE_INF,
)
from os import path
from backend.entidades.entidades import (
    Entidad,
    ConejoChico,
    EntidadMovimiento,
    LovoHorizontal,
    LovoVertical,
    Zanahoria,
    Canon,
    BombaCongelacion,
    BombaManzana,
    Item,
    Lobo,
    Explosion,
    Congelacion,
)
from frontend.components.components import Sprite, ItemInventario
from backend.util.funciones_cliente import calcular_puntaje, obtener_laberinto_nivel


class Mundo(QObject):
    evento_se_cargo_el_mundo = pyqtSignal(list)
    evento_cambio_nivel_duracion_y_puntaje = pyqtSignal(int, int, float)
    evento_cambio_vidas_conejo_chico = pyqtSignal(int)
    evento_actualizar_inventario = pyqtSignal(object)
    evento_cerrar_juego = pyqtSignal(str, float)
    evento_poner_item = pyqtSignal(object)
    evento_guardar_usuario = pyqtSignal(float, int)

    def __init__(
        self,
        nivel: int,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.ponderaciones = (
            PONDERADOR_LABERINTO_1,
            PONDERADOR_LABERINTO_2,
            PONDERADOR_LABERINTO_3,
        )

        self._nivel: int = nivel
        self.sprites: List[List[Sprite]] = []
        self.pausa = False

        self.duracion_nivel = 0
        self.velocidad_lobo = 0
        self.puntaje = 0
        self.puntaje_original = 0

        self.mutex = QMutex()
        self.conejo_chico = ConejoChico(
            fila=15,
            col=15,
            velocidad=VELOCIDAD_CONEJO,
            vidas=max(1, CANTIDAD_VIDAS - self.nivel + 1),
            mutex=self.mutex,
        )
        self.conejo_chico.evento_entidad_se_movio.connect(self.mover)
        self.conejo_chico.evento_recoger_item.connect(self.coger_item)
        self.conejo_chico.evento_cambio_vida.connect(self.cambio_vida)

        self.bucle_duracion_nivel = QTimer()
        self.bucle_duracion_nivel.setInterval(1000)
        self.bucle_duracion_nivel.timeout.connect(self.cambio_duracion)

    @property
    def nivel(self):
        return self._nivel

    @nivel.setter
    def nivel(self, nivel):
        self._nivel = nivel if 0 < nivel < 4 else 1

    def cambio_duracion(self):
        if self.pausa:
            return
        if not self.conejo_chico.inmortalidad:
            self.duracion_nivel = (
                self.duracion_nivel - 1 if self.duracion_nivel - 1 >= 0 else 0
            )

        if self.duracion_nivel == 0:
            self.conejo_chico.vidas -= 1

            duracion_nivel = DURACION_NIVEL_INICIAL * self.ponderaciones[0]
            for i in range(1, self.nivel):
                duracion_nivel = duracion_nivel * self.ponderaciones[i]

            self.duracion_nivel = duracion_nivel

        self.puntaje = self.puntaje_original + (
            calcular_puntaje(
                self.duracion_nivel,
                self.conejo_chico.vidas,
                self.conejo_chico.cantidad_lobos_eliminados,
                PUNTAJE_LOBO,
            )
            if self.conejo_chico.inmortalidad == False
            else PUNTAJE_INF
        )
        self.puntaje = round(self.puntaje, 2)
        self.evento_cambio_nivel_duracion_y_puntaje.emit(
            self.nivel, self.duracion_nivel, self.puntaje
        )

    def cambio_vida(self, anterior, nueva, entidad: Entidad):
        if self.pausa:
            return
        if isinstance(entidad, EntidadMovimiento):
            entidad.bucle_velocidad.stop()
        if isinstance(entidad, ConejoChico):
            self.evento_cambio_vidas_conejo_chico.emit(nueva)
            if nueva == 0:
                self.evento_cerrar_juego.emit(
                    f"Lo lamento {self.conejo_chico.nombre} haz perdido, Gato Chico ha muerto :c",
                    self.puntaje_original,
                )
                self.alternar_pausa()
            for fila, elementos in enumerate(self.sprites):
                for col, sprite in enumerate(elementos):
                    if sprite.fondo == "E":
                        fila_e, col_e = fila, col
                    for e in sprite.entidades:
                        if isinstance(e, Lobo):
                            e.recuperar_velociad_original()
            self.sprites[self.conejo_chico.fila][self.conejo_chico.col].borrar_entidad(
                self.conejo_chico
            )
            self.conejo_chico.direccion = ""
            self.conejo_chico.fila = fila_e
            self.conejo_chico.col = col_e
            self.sprites[fila_e][col_e].agregar_entidad(self.conejo_chico)
            entidad.bucle_velocidad.start()
            return
        if nueva == 0:
            if isinstance(entidad, Lobo):
                self.conejo_chico.cantidad_lobos_eliminados += 1
            self.sprites[entidad.fila][entidad.col].borrar_entidad(entidad)
            return
        if isinstance(entidad, EntidadMovimiento):
            entidad.start()

    def cargar_laberinto(self) -> Tuple[List[List[str]], int, int]:
        self.pausa = True
        self.bucle_duracion_nivel.stop()
        self.conejo_chico.cantidad_lobos_eliminados = 0
        for fila, elementos in enumerate(self.sprites):
            for col, sprite in enumerate(elementos):
                sprite.entidades = []
                sprite.pintar()
        self.sprites = []
        duracion_nivel = DURACION_NIVEL_INICIAL * self.ponderaciones[0]
        velocidad_lobo = VELOCIDAD_LOBO / self.ponderaciones[0]
        for i in range(1, self.nivel):
            duracion_nivel = duracion_nivel * self.ponderaciones[i]
        for i in range(1, self.nivel):
            velocidad_lobo = velocidad_lobo / self.ponderaciones[i]
        self.duracion_nivel = round(duracion_nivel)
        self.velocidad_lobo = round(velocidad_lobo)
        laberinto = obtener_laberinto_nivel(self.nivel)
        self.sprites: List[List[Sprite]] = [
            [Sprite(fondo) for fondo in elementos] for elementos in laberinto
        ]
        for fila, elementos in enumerate(laberinto):
            for col, elemento in enumerate(elementos):
                entidades = []
                if elemento == "C":
                    self.conejo_chico.direccion = ""
                    self.conejo_chico.fila = fila
                    self.conejo_chico.col = col
                    entidades.append(self.conejo_chico)
                    if not self.conejo_chico.bucle_velocidad.isActive():
                        self.conejo_chico.bucle_velocidad.start()
                elif elemento == "LH":
                    lobo = LovoHorizontal(
                        fila=fila, col=col, velocidad=VELOCIDAD_LOBO, mutex=self.mutex
                    )
                    lobo.evento_entidad_se_movio.connect(self.mover)
                    lobo.evento_cambio_vida.connect(self.cambio_vida)
                    entidades.append(lobo)
                elif elemento == "LV":
                    lobo = LovoVertical(
                        fila=fila, col=col, velocidad=VELOCIDAD_LOBO, mutex=self.mutex
                    )
                    lobo.evento_entidad_se_movio.connect(self.mover)
                    lobo.evento_cambio_vida.connect(self.cambio_vida)
                    entidades.append(lobo)
                elif elemento in ["CU", "CD", "CR", "CL"]:
                    canon = Canon(
                        fila=fila,
                        col=col,
                        orientacion=elemento,
                        intervalo_disparo=INTERVALO_DISPARO_CANON,
                    )
                    canon.evento_disparar.connect(self.aparecer_zanahoria)
                    entidades.append(canon)
                elif elemento == "BM":
                    bomba = BombaManzana(fila=fila, col=col)
                    entidades.append(bomba)
                elif elemento == "BC":
                    bomba = BombaCongelacion(fila=fila, col=col)
                    entidades.append(bomba)
                elif elemento not in "SPE-":
                    print(f"El elemento {elemento} no existe para graficar")
                self.sprites[fila][col].entidades = entidades
                self.sprites[fila][col].evento_poner_item.connect(
                    self.lanzar_evento_poner_item
                )
        self.evento_se_cargo_el_mundo.emit(self.sprites)
        self.bucle_duracion_nivel.start()
        self.pausa = False

    def mover(
        self,
        fila_actual: int,
        col_actual: int,
        fila_nueva: int,
        col_nueva: int,
        entidad: Entidad,
    ):
        if self.pausa:
            return
        try:
            casilla = self.sprites[fila_nueva][col_nueva]
            if casilla.fondo == "P" or casilla.atrabesable == False:
                self._no_se_puede_mover(fila_actual, col_actual, entidad)
                return
            elif casilla.fondo == "S" and isinstance(entidad, ConejoChico):
                self.pausa = True
                self.puntaje_original = self.puntaje
                self.evento_guardar_usuario.emit(self.puntaje, self.nivel)
                if self.nivel + 1 > 3:
                    self.evento_cerrar_juego.emit(
                        f"Fenomenal {self.conejo_chico.nombre} haz ganado, gg :3",
                        self.puntaje,
                    )
                    return
                self.nivel = self.nivel + 1
                self.cargar_laberinto()
                return
            if isinstance(entidad, EntidadMovimiento):
                entidad.animacion()
            self.sprites[fila_actual][col_actual].borrar_entidad(entidad)
            entidad.fila = fila_nueva
            entidad.col = col_nueva
            casilla.agregar_entidad(entidad)
            for entidad_casilla in casilla.entidades:
                entidad.interactuar(entidad_casilla)
        except IndexError:
            self._no_se_puede_mover(fila_actual, col_actual, entidad)

    def _no_se_puede_mover(self, fila_actual, col_actual, entidad: Entidad):
        if isinstance(entidad, EntidadMovimiento):
            entidad.animacion(0)
            self.sprites[fila_actual][col_actual].pintar()
        if isinstance(entidad, LovoHorizontal):
            if entidad.direccion == "D":
                entidad.direccion_A()
            else:
                entidad.direccion_D()
        if isinstance(entidad, LovoVertical):
            if entidad.direccion == "W":
                entidad.direccion_S()
            else:
                entidad.direccion_W()
        if isinstance(entidad, Zanahoria):
            self.sprites[fila_actual][col_actual].borrar_entidad(entidad)

    def aparecer_zanahoria(self, fila_zanahoria, col_zonahoria, entidad: Entidad):
        if not isinstance(entidad, Canon) or self.pausa:
            return
        try:
            casilla: Sprite = self.sprites[fila_zanahoria][col_zonahoria]
        except IndexError:
            return
        zanahoria = Zanahoria(
            fila=fila_zanahoria,
            col=col_zonahoria,
            direccion=entidad.orientacion,
            velocidad=VELOCIDAD_ZANAHORIA,
            mutex=self.mutex,
        )
        zanahoria.evento_entidad_se_movio.connect(self.mover)
        casilla.agregar_entidad(zanahoria)
        for entidad_casilla in casilla.entidades:
            entidad.interactuar(entidad_casilla)

    def coger_item(self, conejo: ConejoChico):
        if self.pausa:
            return
        casilla: Sprite = self.sprites[conejo.fila][conejo.col]
        items: List[Item] = list(
            filter(lambda x: isinstance(x, Item), casilla.entidades)
        )
        for item in items:
            casilla.borrar_entidad(item)
        items: List[ItemInventario] = list(
            map(lambda x: ItemInventario(x.nombre_sprite), items)
        )
        conejo.inventario.extend(items)
        self.evento_actualizar_inventario.emit(conejo.inventario)

    def alternar_pausa(self):
        self.pausa = not self.pausa

    def borrar_villanos(self):
        self.alternar_pausa()
        for fila, elementos in enumerate(self.sprites):
            for col, sprite in enumerate(elementos):
                x = filter(
                    lambda e: not isinstance(e, (Lobo, Zanahoria)), sprite.entidades
                )
                sprite.entidades = list(x)
                for e in sprite.entidades:
                    if isinstance(e, Canon):
                        e.bucle_disparo.stop()
        self.alternar_pausa()

    def infinito(self):
        self.conejo_chico.cambiar_mortalidad(True)

    def lanzar_evento_poner_item(self, casilla: Sprite):
        self.evento_poner_item.emit(casilla)

    def usar_item(self, item: ItemInventario, celda: Sprite):
        if item not in self.conejo_chico.inventario:
            return
        self.conejo_chico.inventario.remove(item)
        self.evento_actualizar_inventario.emit(self.conejo_chico.inventario)
        x, y = None, None
        for fila, elementos in enumerate(self.sprites):
            for col, sprite in enumerate(elementos):
                if sprite == celda:
                    x, y = fila, col
        for col in range(y, ANCHO_LABERINTO):
            casilla: Sprite = self.sprites[x][col]
            if casilla.fondo == "P":
                break
            self.agreagar_efecto(item, casilla, x, col)
        for col in range(y, 0, -1):
            casilla: Sprite = self.sprites[x][col]
            if casilla.fondo == "P":
                break
            self.agreagar_efecto(item, casilla, x, col)
        for fila in range(x, LARGO_LABERINTO):
            casilla: Sprite = self.sprites[fila][y]
            if casilla.fondo == "P":
                break
            self.agreagar_efecto(item, casilla, fila, y)
        for fila in range(x, 0, -1):
            casilla: Sprite = self.sprites[fila][y]
            if casilla.fondo == "P":
                break
            self.agreagar_efecto(item, casilla, fila, y)

    def agreagar_efecto(self, item, casilla: Sprite, x, y):
        if item.fondo == "manzana.png":
            explosion = Explosion(fila=x, col=y, tiempo_bomba=TIEMPO_BOMBA)
            explosion.evento_cambio_vida.connect(self.cambio_vida)
            casilla.agregar_entidad(explosion)
            for entidad_casilla in casilla.entidades:
                entidad_casilla.interactuar(explosion)
        elif item.fondo == "congelacion.png":
            congelacion = Congelacion(fila=x, col=y, tiempo_bomba=TIEMPO_BOMBA)
            congelacion.evento_cambio_vida.connect(self.cambio_vida)
            casilla.agregar_entidad(congelacion)
            for entidad_casilla in casilla.entidades:
                entidad_casilla.interactuar(congelacion)

    def vida_conejo(self):
        self.conejo_chico.vidas = max(1, CANTIDAD_VIDAS - self.nivel + 1)
