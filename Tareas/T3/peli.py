import api
import requests


class Peliculas:
    def __init__(self, host, port):
        self.base = f"http://{host}:{port}"

    def saludar(self) -> dict:
        res = requests.get(self.base + "/")

        if res.status_code == 200:
            data = res.json()
        return {"status-code": res.status_code, "saludo": data.get("result")}

    def verificar_informacion(self, pelicula: str) -> bool:
        res = requests.get(self.base + "/peliculas")

        if res.status_code == 200:
            data = res.json()

        return pelicula in data.get("result")

    def dar_informacion(self, pelicula: str) -> dict:
        res = requests.get(self.base + "/informacion", params={"pelicula": pelicula})

        data = res.json()
        return {"status-code": res.status_code, "mensaje": data.get("result")}

    def dar_informacion_aleatoria(self) -> dict:
        res0 = requests.get(self.base + "/aleatorio")
        data0 = res0.json()

        if res0.status_code == 200:
            res1 = requests.get(data0.get("result"))
            data1 = res1.json()
            return {"status-code": res1.status_code, "mensaje": data1.get("result")}

        return {"status-code": res0.status_code, "mensaje": data0.get("result")}

    def agregar_informacion(self, pelicula: str, sinopsis: str, access_token: str):
        res = requests.post(
            self.base + "/update",
            data={"pelicula": pelicula, "sinopsis": sinopsis},
            headers={"Authorization": access_token},
        )
        data = res.json()
        if res.status_code == 401:
            return "Agregar pelicula no autorizado"
        elif res.status_code == 400:
            return data.get("result")
        return "La base de la API ha sido actualizada"

    def actualizar_informacion(self, pelicula: str, sinopsis: str, access_token: str):
        res = requests.patch(
            self.base + "/update",
            data={"pelicula": pelicula, "sinopsis": sinopsis},
            headers={"Authorization": access_token},
        )
        data = res.json()
        if res.status_code == 401:
            return "Editar información no autorizado"
        elif res.status_code == 200:
            return "La base de la API ha sido actualizada"
        return data.get("result")

    def eliminar_pelicula(self, pelicula: str, access_token: str):
        res = requests.delete(
            self.base + "/remove",
            data={"pelicula": pelicula},
            headers={"Authorization": access_token},
        )
        data = res.json()
        if res.status_code == 401:
            return "Eliminar pelicula no autorizado"
        elif res.status_code == 200:
            return "La base de la API ha sido actualizada"
        return data.get("result")


if __name__ == "__main__":
    HOST = "localhost"
    PORT = 4444
    DATABASE = {
        "Mamma Mia": "Mamma Mia es una Comedia musical con ABBA",
        "Monsters Inc": "Monsters Inc trata sobre monstruos que asustan, niños y risas",
        "Incredibles": "Incredibles trata de una familia de superhéroes que salva el mundo",
        "Avengers": "Avengers trata de superhéroes que luchan contra villanos poderosos",
        "Titanic": "Titanic es sobre amor trágico en el hundimiento del Titanic",
        "Akira": "Akira es una película de ciencia ficción japonesa con poderes psíquicos",
        "High School Musical": "High School Musical es un drama musical adolescente en East High",
        "The Princess Diaries": "The Princess Diaries es sobre Mia, una joven que descubre que es"
        "princesa de Genovia",
        "Iron Man": "Iron Man trata sobre un hombre construye traje de alta tecnología "
        "para salvar al mundo",
        "Tarzan": "Tarzan es sobre un hombre criado por simios en la jungla",
        "The Pianist": "The Pianist es sobre un músico judío que sobrevive en Varsovia"
        " durante el Holocausto",
    }
    thread = api.Server(HOST, PORT, DATABASE)
    thread.start()

    Peliculas = Peliculas(HOST, PORT)
    print(Peliculas.saludar())
    print(Peliculas.dar_informacion_aleatoria())
    print(
        Peliculas.actualizar_informacion(
            "Titanic",
            "Titanic es sobre amor trágico inspitado"
            " en el historico hundimiento del Titanic",
            "tereiic2233",
        )
    )
    print(Peliculas.verificar_informacion("Tarzan"))
    print(Peliculas.dar_informacion("The Princess Diaries"))
    print(Peliculas.dar_informacion("Monsters Inc"))
    print(
        Peliculas.agregar_informacion(
            "Matilda",
            "Matilda es sobre una niña con poderes"
            "telequinéticos que enfrenta a su malvada directora",
            "tereiic2233",
        )
    )
    print(Peliculas.dar_informacion("Matilda"))
