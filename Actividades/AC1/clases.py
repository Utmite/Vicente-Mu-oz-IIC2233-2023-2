from abc import ABC, abstractmethod
import random


class Vehiculo(ABC):
    identificador = 0

    def __init__(self, rendimiento, marca, energia=120) -> None:
        self.rendimiento = rendimiento
        self.marca = marca
        self._energia = energia
        self.identificador = Vehiculo.identificador
        Vehiculo.identificador = Vehiculo.identificador + 1

    @abstractmethod
    def recorrer(self, kilometros) -> None:
        pass

    @property
    def autonomia(self) -> float:
        return self._energia * self.rendimiento

    @property
    def energia(self) -> int:
        return self._energia

    @energia.setter
    def energia(self, valor) -> None:
        if valor < 0:
            valor = 0
        self._energia = valor


class AutoBencina(Vehiculo):
    def __init__(self, bencina_favorita: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.bencina_favorita: int = bencina_favorita

    def recorrer(self, kilometros) -> str:
        if self.autonomia < kilometros:
            kilometros = self.autonomia

        gasta = int(kilometros / self.rendimiento)
        self.energia = self.energia - gasta
        return f"Anduve por {kilometros}Km y gasté {gasta}L de bencina"


class AutoElectrico(Vehiculo):
    def __init__(self, vida_util_bateria: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.vida_util_bateria = vida_util_bateria

    def recorrer(self, kilometros) -> str:
        if self.autonomia < kilometros:
            kilometros = self.autonomia

        gasta = int(kilometros / self.rendimiento)
        self.energia = self.energia - gasta

        return f"Anduve por {kilometros}Km y gasté {gasta}W de energía eléctrica"


class Camioneta(AutoBencina):
    def __init__(self, capacidad_maleta, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.capacidad_maleta = capacidad_maleta


class FaitHibrido(AutoBencina, AutoElectrico):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(vida_util_bateria=5, *args, **kwargs)

    def recorrer(self, kilometros) -> str:
        a = AutoBencina.recorrer(self, kilometros // 2)
        e = AutoElectrico.recorrer(self, kilometros // 2)

        return a + e


class Telsa(AutoElectrico):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def recorrer(self, kilometros) -> str:
        return super().recorrer(kilometros) + "de forma inteligente"
