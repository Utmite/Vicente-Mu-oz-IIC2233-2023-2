import api
import requests
import re


class Yolanda:
    def __init__(self, host, port):
        self.base = f"http://{host}:{port}"
        self.regex_validador_fechas = (
            r"\b\d{1,2}\s+de\s+[a-zA-Z]+\s+de\s+(?:\d{2}|\b(?:19|20)\d{2})\b"
        )
        self.regex_extractor_signo = r"(?:Los|Las)\s+(\b\w+\b)\s+pueden\s+[^.]+."

    def saludar(self) -> dict:
        res = requests.get(f"{self.base}/")
        contenido = res.json()
        return {"status-code": res.status_code, "saludo": contenido["result"]}

    def verificar_horoscopo(self, signo: str) -> bool:
        res = requests.get(f"{self.base}/signos")
        contenido = res.json()

        return signo in contenido["result"]

    def dar_horoscopo(self, signo: str) -> dict:
        res = requests.get(f"{self.base}/horoscopo", params={"signo": signo})
        contenido = res.json()

        return {"status-code": res.status_code, "mensaje": contenido["result"]}

    def dar_horoscopo_aleatorio(self) -> dict:
        res1 = requests.get(f"{self.base}/aleatorio")
        contenido1 = res1.json()

        if res1.status_code != 200:
            return {"status-code": res1.status_code, "mensaje": contenido1["result"]}
        else:
            res2 = requests.get(f"{contenido1['result']}")
            contenido2 = res2.json()
            return {"status-code": res2.status_code, "mensaje": contenido2["result"]}

    def agregar_horoscopo(self, signo: str, mensaje: str, access_token: str) -> str:
        res = requests.post(
            f"{self.base}/update",
            headers={"Authorization": access_token},
            data={"signo": signo, "mensaje": mensaje},
        )

        if res.status_code == 401:
            return "Agregar horóscopo no autorizado"
        elif res.status_code == 400:
            contenido = res.json()
            return contenido["result"]

        return "La base de YolandAPI ha sido actualizada"

    def actualizar_horoscopo(self, signo: str, mensaje: str, access_token: str) -> str:
        res = requests.put(
            f"{self.base}/update",
            headers={"Authorization": access_token},
            data={"signo": signo, "mensaje": mensaje},
        )

        if res.status_code == 401:
            return "Editar horóscopo no autorizado"
        elif res.status_code == 400:
            contenido = res.json()
            return contenido["result"]

        return "La base de YolandAPI ha sido actualizada"

    def eliminar_signo(self, signo: str, access_token: str) -> str:
        res = requests.delete(
            f"{self.base}/remove",
            headers={"Authorization": access_token},
            data={"signo": signo},
        )

        if res.status_code == 401:
            return "Eliminar signo no autorizado"
        elif res.status_code == 400:
            contenido = res.json()
            return contenido["result"]
        return "La base de YolandAPI ha sido actualizada"


if __name__ == "__main__":
    HOST = "localhost"
    PORT = 4444
    DATABASE = {
        "acuario": "Hoy será un hermoso día",
        "leo": "No salgas de casa.... te lo recomiendo",
    }
    thread = api.Server(HOST, PORT, DATABASE)
    thread.start()

    yolanda = Yolanda(HOST, PORT)
    print(yolanda.saludar())
    print(yolanda.dar_horoscopo_aleatorio())
    print(yolanda.verificar_horoscopo("acuario"))
    print(yolanda.verificar_horoscopo("pokemon"))
    print(yolanda.dar_horoscopo("acuario"))
    print(yolanda.dar_horoscopo("pokemon"))
    print(yolanda.agregar_horoscopo("a", "aaaaa", "pepaiic2233"))
    print(yolanda.dar_horoscopo("a"))
