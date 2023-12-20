from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import QUrl
from os import path


class SonidoGanar(QSoundEffect):
    def __init__(self):
        super().__init__()
        sonido_path = path.join(
            path.dirname(path.abspath(__file__)),
            f"../assets/sonidos/victoria.wav",
        )

        self.setSource(QUrl.fromLocalFile(sonido_path))
        self.play()


class SonidoPerder(QSoundEffect):
    def __init__(self):
        super().__init__()
        sonido_path = path.join(
            path.dirname(path.abspath(__file__)),
            f"../assets/sonidos/derrota.wav",
        )
        self.setSource(QUrl.fromLocalFile(sonido_path))
        self.play()
