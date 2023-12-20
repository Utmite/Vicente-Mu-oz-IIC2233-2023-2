from collections import defaultdict, deque
from typing import List


class Jugador:
    def __init__(self, nombre: str, velocidad: int) -> None:
        self.nombre = nombre
        self.velocidad = velocidad

    def __repr__(self) -> None:
        return f"Jugador: {self.nombre}, Velocidad: {self.velocidad}"


class Equipo:
    def __init__(self) -> None:
        self.jugadores = dict()
        self.dict_adyacencia = defaultdict(set)

    def agregar_jugador(self, id_jugador: int, jugador: Jugador) -> bool:
        """Agrega un nuevo jugador al equipo."""
        if self.jugadores.get(id_jugador) is None:
            self.jugadores[id_jugador] = jugador
            return False

        return True

    def agregar_vecinos(self, id_jugador: int, vecinos: List[int]) -> int:
        """Agrega una lista de vecinos a un jugador."""
        if id_jugador not in self.jugadores.keys():
            self.dict_adyacencia[id_jugador]
            return -1

        lon0 = len(self.dict_adyacencia[id_jugador])
        self.dict_adyacencia[id_jugador] = set(self.dict_adyacencia[id_jugador]).union(
            vecinos
        )
        lon1 = len(self.dict_adyacencia[id_jugador])

        return lon1 - lon0

    def peor_amigo(self, id_jugador: int) -> Jugador | None:
        """Retorna al vecino con la velocidad menos similar."""
        jugador = self.jugadores[id_jugador]
        peor_enemigo_id = max(
            self.dict_adyacencia[id_jugador],
            key=lambda i: abs(self.jugadores[i].velocidad - jugador.velocidad),
            default=None,
        )
        if peor_enemigo_id is None:
            return None

        peor_enemigo = self.jugadores[peor_enemigo_id]

        if jugador.nombre == peor_enemigo.nombre:
            return None
        return peor_enemigo

    def mejor_compañero(self, id_jugador: int) -> Jugador:
        """Retorna al compañero de equipo con la menor diferencia de velocidad."""
        jugador = self.jugadores[id_jugador]
        mejor_id = min(
            self.dict_adyacencia[id_jugador],
            key=lambda i: abs(self.jugadores[i].velocidad - jugador.velocidad),
            default=None,
        )
        if mejor_id is None:
            return None

        mejor = self.jugadores[mejor_id]

        if jugador.nombre == mejor.nombre:
            return None
        return mejor

    def mejor_conocido(self, id_jugador: int) -> Jugador:
        """Retorna al conocido con la menor diferencia de velocidad."""
        visitados = set()
        cola = deque([(id_jugador, 0)])

        while cola:
            jugador, distancia_actual = cola.popleft()

            if jugador not in visitados:
                visitados.add(jugador)
                for adyacente in self.dict_adyacencia[jugador]:
                    cola.append((adyacente, distancia_actual + 1))

        jugador = self.jugadores[id_jugador]
        visitados.remove(id_jugador)
        mejor_id = min(
            visitados,
            key=lambda i: abs(self.jugadores[i].velocidad - jugador.velocidad),
            default=None,
        )
        if mejor_id is None:
            return None

        mejor = self.jugadores[mejor_id]

        return mejor

    def distancia(self, id_jugador_1: int, id_jugador_2: int) -> int:
        """Retorna el tamaño del camino más corto entre los jugadores."""
        if id_jugador_1 not in self.jugadores or id_jugador_2 not in self.jugadores:
            return -1

        visitados = set()
        cola = deque([(id_jugador_1, 0)])
        distancias = []

        while cola:
            jugador, distancia_actual = cola.popleft()

            if jugador == id_jugador_2:
                distancias.append(distancia_actual)

            if jugador not in visitados:
                visitados.add(jugador)
                for adyacente in self.dict_adyacencia[jugador]:
                    cola.append((adyacente, distancia_actual + 1))
        if len(distancias) != 0:
            return min(distancias)

        return -1


if __name__ == "__main__":
    equipo = Equipo()
    jugadores = {
        0: Jugador("Ana", 1),
        1: Jugador("Antonio", 3),
        2: Jugador("Alfredo", 6),
        3: Jugador("Ariel", 10),
    }
    adyacencia = {
        0: [1],
        1: [0, 2],
        2: [1],
    }
    for idj, jugador in jugadores.items():
        equipo.agregar_jugador(id_jugador=idj, jugador=jugador)
    for idj, vecinos in adyacencia.items():
        equipo.agregar_vecinos(id_jugador=idj, vecinos=vecinos)

    print(f"El peor amigo de Antonio es {equipo.peor_amigo(1)}")
    print(f"El mejor compañero de Ana es {equipo.mejor_compañero(0)}")
    print(f"El mejor conocido de Alfredo es {equipo.mejor_conocido(2)}")
    print(f"La distancia entre Alfredo y Ana es {equipo.distancia(2, 0)}")
    print(f"La distancia entre Antonio y Ariel es {equipo.distancia(1, 3)}")
    print(f"La distancia entre Antonio y Amalia es {equipo.distancia(1, 5)}")
