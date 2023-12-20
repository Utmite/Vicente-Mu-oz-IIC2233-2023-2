from os.path import join

# from entities import Item


def cargar_items() -> list:
    items = []

    with open(
        "/home/palios/universidad/progra_avanzada/Utmite-iic2233-2023-2/EX1/release/utils/items.dcc"
    ) as archivo:
        for linea in archivo.readlines():
            nombre, precio, puntos = linea.strip().split(",")
            # items.append(Item(nombre, int(precio), int(puntos)))

    return items
