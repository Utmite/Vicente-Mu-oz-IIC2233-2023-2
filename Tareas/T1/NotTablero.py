
import copy
from pieza_explosiva import PiezaExplosiva

class NotTablero:
    def __init__(self, tablero: list) -> None:
        # filas         #columnas
        self.dimensiones = [len(tablero), len(tablero[0])]
        self.tablero = tablero

    # TODO: completar esta property
    @property
    def filas(self):
        return self.dimensiones[0]

    @property
    def columnas(self):
        return self.dimensiones[1]

    @property
    def peones_invalidos(self) -> int:
        tablero_copia = copy.deepcopy(self.tablero)
        """
        - E -
        E E -
        - - -

        ilegal pues el 1,1 tiene 2 vecinos
        """
        invalidos = 0
        for x in range(self.filas):
            for y in range(self.columnas):
                elemento = tablero_copia[x][y]

                if elemento != "PP":
                    continue
                x1 = tablero_copia[x + 1][y] if 0 <= x + 1 < self.filas else "--"
                x2 = tablero_copia[x - 1][y] if 0 <= x - 1 < self.filas else "--"
                x3 = tablero_copia[x][y + 1] if 0 <= y + 1 < self.columnas else "--"
                x4 = tablero_copia[x][y - 1] if 0 <= y - 1 < self.columnas else "--"

                vecinos = [x1, x2, x3, x4]
                vecinos = list(filter(lambda i: i == "PP", vecinos))

                if len(vecinos) > 1:
                    invalidos = invalidos + 1

        return invalidos

    # NOTE hecho
    @property
    def tablero_transformado(self) -> list:
        tablero_copia = copy.deepcopy(self.tablero)
        for x in range(len(tablero_copia)):
            for y in range(len(tablero_copia[0])):
                if (
                    tablero_copia[x][y][1:2] in "0123456789"
                    and tablero_copia[x][y][1:2] != ""
                ):
                    # EL QUE PUSO EL DE DOS DIGITTOS UFF!!
                    # HOLA :)
                    tipo, alcance = tablero_copia[x][y][0], int(tablero_copia[x][y][1:])
                    tablero_copia[x][y] = PiezaExplosiva(
                        tipo=tipo, alcance=alcance, posicion=[x, y]
                    )
        return tablero_copia
    
    @property
    def piezas_explosivas_invalidas(self) -> int:
        invalidos = 0
        piezas = self.obtener_piezas_explosiva()

        for pieza in piezas:
            pieza: PiezaExplosiva

            if pieza.alcance != self.celdas_afectadas(pieza.fila, pieza.columna):
                invalidos = invalidos + 1
        return invalidos

    def celdas_afectadas(self, fila: int, columna: int) -> int:
        """
        Tiro un rayo para arriba, abajo, izquierda, derecha
        Tiro rayo para diagonal derecha arriba, diagonal izquierda arriba
        diagonal derecha abajo, diagonal izquierda abajo
        """
        tablero = self.tablero_transformado
        if not isinstance(tablero[fila][columna], PiezaExplosiva):
            return -1

        pieza: PiezaExplosiva = tablero[fila][columna]

        columna = []
        filas = []
        diagonales = []

        if pieza.tipo in "VR":
            for x in range(pieza.fila, self.filas):
                if str(tablero[x][pieza.columna]) in "-PP-":
                    break
                columna.append((x, pieza.columna))

            for x in range(pieza.fila, -1, -1):
                if str(tablero[x][pieza.columna]) in "-PP-":
                    break
                columna.append((x, pieza.columna))

        if pieza.tipo in "HR":
            for y in range(pieza.columna, self.columnas):
                if str(tablero[pieza.fila][y]) in "-PP-":
                    break
                filas.append((pieza.fila, y))

            for y in range(pieza.columna, -1, -1):
                if str(tablero[pieza.fila][y]) in "-PP-":
                    break
                filas.append((pieza.fila, y))

        if pieza.tipo == "R":
            for x in range(pieza.fila, self.filas):
                for y in range(pieza.columna, self.columnas):
                    if abs(x - pieza.fila) == abs(y - pieza.columna):
                        if str(tablero[x][y]) in "-PP-":
                            break
                        
                        diagonales.append((x, y))
                else:
                    continue
                break
            for x in range(pieza.fila, -1, -1):
                for y in range(pieza.columna, self.columnas):
                    if abs(x - pieza.fila) == abs(y - pieza.columna):
                        if str(tablero[x][y]) in "-PP-":
                            break
                        diagonales.append((x, y))
                else:
                    continue
                break
            for x in range(pieza.fila, self.filas):
                for y in range(pieza.columna, -1, -1):
                    if abs(x - pieza.fila) == abs(y - pieza.columna):
                        if str(tablero[x][y]) in "-PP-":
                            break
                        diagonales.append((x, y))
                else:
                    continue
                break
            for x in range(pieza.fila, -1, -1):
                for y in range(pieza.columna, -1, -1):
                    if abs(x - pieza.fila) == abs(y - pieza.columna):
                        if str(tablero[x][y]) in "-PP-":
                            break

                        diagonales.append((x, y))
                else:
                    continue
                break

        columna = list(set(columna))
        filas = list(set(filas))
        diagonales = list(set(diagonales))

        todos = columna + filas + diagonales
        
        todos = set(todos)

        return len(todos)


    def obtener_piezas_explosiva(self) -> list:
        ORDEN = {"V": 0, "H": 1, "R": 2}
        tablero_copia = self.tablero_transformado
        tablero_plano = [elemento for fila in tablero_copia for elemento in fila]
        piezas = list(
            filter(lambda i: i not in ["PP", "--", "-PP", "PP-"], tablero_plano)
        )

        piezas = list(sorted(piezas, key=lambda i: ORDEN.get(i.tipo, 0)))

        return piezas

