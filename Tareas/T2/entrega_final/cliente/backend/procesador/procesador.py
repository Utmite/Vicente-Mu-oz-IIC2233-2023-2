import json
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication
from backend.net.cliente import Cliente
from backend.util.funciones_cliente import validacion_formato


class Procesador(QObject):
    cliente = None
    puede_jugar = pyqtSignal(bool, str, str, float, int)
    salon_de_la_fama = pyqtSignal(list)

    def __init__(self, host: str, port: int):
        super().__init__()
        Procesador.cliente = Cliente(host=host, port=port)
        if not Procesador.cliente.isRunning():
            Procesador.cliente.start()
            Procesador.cliente.se_recivio_mensaje.connect(self.permitido_jugar)
            Procesador.cliente.se_recivio_mensaje.connect(self.llego_salon_de_la_fama)
        self.nombre = ""

    def cerrar_aplicacion(self):
        QApplication.quit()

    def mandar_nombre(self, nombre: str):
        es_valido = validacion_formato(nombre)

        if not es_valido:
            self.puede_jugar.emit(
                False,
                """El nombre no esta valido, debe ser alguna mayuscula, estar en 3
y 16 caracteres y tener algun numero""",
                nombre,
                1,
                0,
            )
            return

        self.cliente.mandar_mensaje_json({"nombre": nombre})

    def pedir_salon_de_la_fama(self) -> dict:
        self.cliente.mandar_mensaje_json({"pedir_salon_de_la_fama": True})

    def permitido_jugar(self, mensaje: dict):
        if (n := mensaje.get("permitido_jugar")) is not None:
            respuesta = "Ingresando..." if n else "Tu nombre de usuario esta baneado"

            nombre = mensaje.get("nombre")
            puntos = mensaje.get("puntos", 0)
            nivel = mensaje.get("nivel", 0)

            # print(f"puede {n}, respuesta: {respuesta}, nombre: {nombre}, puntos: {puntos}, nivel: {nivel}")
            self.puede_jugar.emit(n, respuesta, nombre, float(puntos), int(nivel))
            return
        self.nombre = mensaje.get("nombre")

    def llego_salon_de_la_fama(self, mensaje: dict):
        if mensaje.get("salon_de_la_fama") is None:
            return

        salon_de_la_fama = mensaje["salon_de_la_fama"]

        salon_de_la_fama = map(lambda x: json.loads(x), salon_de_la_fama)

        salon_de_la_fama = sorted(
            salon_de_la_fama, key=lambda x: float(x["puntos"]), reverse=True
        )

        self.salon_de_la_fama.emit(salon_de_la_fama)

    def mandar_usuario(self, puntaje: float, nivel: int):
        self.cliente.mandar_mensaje_json(
            {
                "nombre": self.nombre,
                "puntaje": puntaje,
                "nivel": nivel,
                "guardar_usuario": True,
            }
        )
