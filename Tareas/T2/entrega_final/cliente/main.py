import sys
import json
from PyQt6.QtWidgets import QApplication
from frontend.views.MainWindow import MainWindow
from frontend.views.JuegoWindow import JuegoWindow
from frontend.views.FinJuego import FinJuego
from backend.procesador.procesador import Procesador
from os import path


def main():
    args = sys.argv
    if len(args) <= 1:
        print(
            "Tienes que ingresar argumentos al llamar la funcion: 'python3 main.py <port>'"
        )
        return
    configuracion_path = path.join(
        path.dirname(path.abspath(__file__)), "configuracion.json"
    )
    with open(configuracion_path, "r", encoding="utf-8") as archivo:
        contenido: dict = json.load(archivo)

    host = contenido["host_servidor"]
    puerto = int(args[1])

    def hook(type, value, traceback):
        print(type)
        print(traceback)
        print(value)

    sys.__excepthook__ = hook
    procesador = Procesador(host=host, port=puerto)

    app = QApplication([])
    window = MainWindow()
    juego = JuegoWindow()
    fin = FinJuego()

    window.cerrar_aplicacion.connect(procesador.cerrar_aplicacion)
    window.apreta_ingresar.connect(procesador.mandar_nombre)

    juego.cerrar_aplicacion.connect(procesador.cerrar_aplicacion)

    juego.juego.mundo.evento_cerrar_juego.connect(juego.ocultar)
    juego.juego.mundo.evento_cerrar_juego.connect(fin.mostrar)
    juego.juego.mundo.evento_guardar_usuario.connect(procesador.mandar_usuario)

    fin.evento_cerrar_aplicacion.connect(procesador.cerrar_aplicacion)

    procesador.puede_jugar.connect(window.iniciar_juego)
    procesador.puede_jugar.connect(juego.cargar_partida_e_iniciar_juego)
    procesador.salon_de_la_fama.connect(window.mostrar_salon_de_la_fama)
    procesador.cliente.evento_se_desconecto.connect(juego.ocultar)
    procesador.cliente.evento_se_desconecto.connect(fin.mostar_desconeccion)
    procesador.cliente.evento_se_desconecto.connect(window.ocultar)

    procesador.pedir_salon_de_la_fama()

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
