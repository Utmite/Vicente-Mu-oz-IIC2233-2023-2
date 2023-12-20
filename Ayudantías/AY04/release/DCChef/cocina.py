from entidades import Cocinero, Mesero
from time import sleep
from random import randint


class Cocina:
    def __init__(self, bodega, recetas):
        super().__init__()
        self.cola_pedidos = list()
        self.cola_pedidos_listos = list()
        self.cocineros = []
        self.meseros = []
        self.bodega = bodega
        self.recetas = recetas
        self.abierta = True

    def iniciar_threads(self):
        for cocinero in self.cocineros:
            cocinero.start()
        for mesero in self.meseros:
            mesero.start()

    def asignar_cocinero(self):
        while self.abierta:
            sleep(1)
            if self.cola_pedidos:
                for cosinero in self.cocineros:
                    cosinero: Cocinero
                    if cosinero.disponible:
                        cosinero.evento_plato_asignado.set()

    def asignar_mesero(self):
        while self.abierta:
            sleep(1)
            if self.cola_pedidos_listos:
                for mesero in self.meseros:
                    mesero: Mesero
                    if mesero.disponible:
                        mesero.evento_manejar_pedido.set()
                        mesero.entregar_pedido(self)

        self.finalizar_jornada_laboral()

    def finalizar_jornada_laboral(self):
        for mesero in self.meseros:
            mesero.trabajando = False

        for cocinero in self.cocineros:
            cocinero.trabajando = False
