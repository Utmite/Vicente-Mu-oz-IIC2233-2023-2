import utils.pretty_print as pt
from utils.loader import cargar_items


def menu():
    while True:
        items = cargar_items()
        pt.print_opciones_menu()

        opcion = input("Indique su opcion: ")
        if opcion == "e":
            pt.print_salida()
            break
        elif opcion == "a":
            pass
        elif opcion == "b":
            pass
        elif opcion == "c":
            pass
        elif opcion == "d":
            pass
        else:
            pt.print_opcion_invalida()


if __name__ == "__main__":
    menu()
