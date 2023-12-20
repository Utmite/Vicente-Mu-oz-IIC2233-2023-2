class PiezaExplosiva:
    def __init__(self, alcance: int, tipo: str, posicion: list) -> None:
        self.alcance = alcance
        self.tipo = tipo
        self.posicion = posicion

    @property
    def fila(self) -> int:
        return self.posicion[0]

    @property
    def columna(self) -> int:
        return self.posicion[1]

    def __str__(self) -> str:
        fila, columna = self.posicion
        texto = f"Soy la pieza {self.tipo}{self.alcance}\n"
        texto += f"\tEstoy en la fila {fila} y columna {columna}\n"
        return texto

    def __repr__(self) -> str:
        return f"PiezaExplosiva(tipo={self.tipo}, fila={self.fila}, columna={self.columna}, alcance={self.alcance})"

    def verificar_alcance(self, fila: int, columna: int) -> bool:
        if self.tipo == "V":
            return self.columna == columna
        elif self.tipo == "H":
            return self.fila == fila
        elif self.tipo == "R":
            if self.fila == fila:
                return True
            if self.columna == columna:
                return True
            if abs(self.columna - columna) == abs(self.fila - fila):
                # Para estar en diagonal me debo mover la misma cantidad
                # por fila que por columna
                return True
            return False

        return False


if __name__ == "__main__":
    """
    Ejemplos:

    Dado el siguiente tablero
    [
        ["--", "V2", "PP", "--", "H2"],
        ["H3", "--", "--", "PP", "R11"]
    ]

    """
    # Ejemplo 1 - Pieza R11
    pieza_1 = PiezaExplosiva(11, "R", [1, 4])
    print(str(pieza_1))

    # Ejemplo 2 - Pieza V2
    pieza_2 = PiezaExplosiva(2, "V", [0, 1])
    print(str(pieza_2))
