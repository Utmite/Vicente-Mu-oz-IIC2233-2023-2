from abc import ABC, abstractmethod
from random import randint
from threading import Thread, Lock, Event, Timer
from time import sleep

from Syllabus.Ayudantías.AY04.release.DCChef.cocina import Cocina


class Persona(ABC, Thread):
    # Completar
    lock_bodega = Lock()
    lock_cola_pedidos = Lock()
    lock_cola_pedidos_listos = Lock()

    def __init__(self, nombre):
        super().__init__()
        self.nombre = nombre
        self.disponible = True
        self.trabajando = True
        self.daemon = True

    @abstractmethod
    def run(self):
        pass


class Cocinero(Persona):
    def __init__(self, nombre, cocina):
        super().__init__(nombre)
        self.lugar_trabajo = cocina
        self.evento_plato_asignado = Event()
        # Completar

    def run(self):
        # Completar
        while self.trabajando:
            self.evento_plato_asignado.wait()  # Espera hasta que le digan cocina
            sleep(randint(1, 3))
            self.cocinar()

    def cocinar(self):
        self.disponible = False
        plato, nombre = self.sacar_plato()
        print(f"Cocinero {self.nombre} cocinando {nombre}")

        self.buscar_ingredientes(
            plato=plato,
            bodega=self.lugar_trabajo.bodega,
            recetas=self.lugar_trabajo.receta,
        )

        self.agregar_plato((plato, nombre))
        self.disponible = True
        self.evento_plato_asignado.clear()

        sleep(randint(1, 3))

    def sacar_plato(self):
        with self.lock_cola_pedidos:
            plato = self.lugar_trabajo.cola_pedidos.pop(0)
        return plato

    def buscar_ingredientes(self, plato, bodega, recetas):
        print(f"Cocinero {self.nombre} buscando a los ingredientes en la bodega")

        with self.lock_bodega:
            ingredientes = recetas[plato]
            # Completar
            for tipo, cantidad in ingredientes:
                bodega[tipo] -= 1
            print(f"Cocinero {self.nombre} buscando los ingredientes en la bodega...")

    def agregar_plato(self, plato):
        # Completar
        with self.lock_cola_pedidos_listos:
            self.lugar_trabajo.cola_pedidos_listos.append(plato)


class Mesero(Persona):
    def __init__(self, nombre):
        super().__init__(nombre)
        self.evento_manejar_pedido = Event()

    def run(self):
        # Completar
        while self.trabajando:
            if self.disponible:
                self.evento_manejar_pedido.set()  # Poner el semaforo en verde

    def agregar_pedido(self, pedido, cocina: Cocina):
        self.evento_manejar_pedido.clear()
        sleep(randint(1, 2))
        with self.lock_cola_pedidos:
            cocina.cola_pedidos_listos.append(pedido)
        self.evento_manejar_pedido.set()

    def entregar_pedido(self, cocina: Cocina):
        self.evento_manejar_pedido.clear()
        tiempo = randint(1, 3)
        with self.lock_cola_pedidos_listos:
            pedido = cocina.cola_pedidos_listos.pop(0)
            timer_entrega = Timer(tiempo, self.pedido_entregado, args=(pedido,))
            timer_entrega.start()
        timer_entrega.start()
        print(f"Mesero {self.nombre} entregando pedido a la mesa {pedido[0]}...")

    def pedido_entregado(self, pedido):
        print(f"El plato {pedido[0]} de la mesa {0} fue entregado")
        self.evento_manejar_pedido.set()
