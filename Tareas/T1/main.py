import sys
from tablero import Tablero


def imprimir_tablero(tablero: list):
    print()
    filas = len(tablero)
    columnas = len(tablero[0])
    tablero = [[str(x) for x in y] for y in tablero]
    tablero_largo = [[len(x) for x in y] for y in tablero]
    max_largo = max([max(x) for x in tablero_largo]) + 2
    tablero_ajustado = [[f"{' '*(max_largo - len(x))}{x}" for x in y] for y in tablero]

    columnas_ = " " * max_largo
    for indice in range(columnas):
        indice = str(indice)
        columnas_ += f"{' '*(max_largo - len(indice))}{indice}"

    print(columnas_)
    for indice in range(filas):
        indice = str(indice)
        fila = f"{' '*(max_largo - len(indice))}{indice}"

        fila += " " + "".join(tablero_ajustado[int(indice)])
        print(fila)
    print()


def main():
    args = sys.argv

    if len(args) == 1:
        print(
            "Tienes que ingresar argumentos al llamar la funcion: 'python3 main.py <Tu Nombre> <Nombre Mapa>'"
        )
        return

    nombre_usuario = args[1]

    if len(nombre_usuario) < 4 and not nombre_usuario.isalpha():
        print("El nombre de usuario tiene menos de 4 caracteres")
        print("El nombre de usuario solo debe tener letras del alfabeto")
        return
    if len(nombre_usuario) < 4:
        print("El nombre de usuario tiene menos de 4 caracteres")
        return
    elif not nombre_usuario.isalpha():
        print("El nombre de usuario solo debe tener letras del alfabeto")
        return

    if len(args) == 2:
        print(
            f"Tienes que ingresar nombre del tablero: 'python3 main.py {nombre_usuario} <Nombre Tablero>'"
        )
        return

    nombre_tablero = args[2]

    T = Tablero([[]])
    try:
        resultado = T.reemplazar(nombre_tablero)
    except FileNotFoundError:
        print(
            f"No se encontro el tablero.txt, recuerda debes ejecutar el archvio en la terminal en la carpeta del main.py y en esa misma carpeta debe haber un tableros.txt para poder cargar el tablero"
        )
        return
    while True:
        if resultado == False:
            print("Tablero no encontrado en tableros.txt")
            break
        try:
            opcion = int(
                input(
                    f"""Usuario: '{nombre_usuario}'
Nombre Tablero: '{nombre_tablero}'
*** Menú de Acciones ***
[1] Mostrar tablero
[2] Limpiar tablero
[3] Solucionar tablero
[4] Salir programa
Indique su opción (1, 2, 3 o 4): """
                )
            )
        except ValueError:
            opcion = 6
        if opcion == 1:
            print("El tablero es: ")
            print("----------------")
            imprimir_tablero(T.tablero)
            print("----------------")

        elif opcion == 2:
            T.limpiar()
            print("¡Se ha limpiado el tablero, asi es como quedo!: ")
            print("----------------")
            imprimir_tablero(T.tablero)
            print("----------------")

        elif opcion == 3:
            sol = T.solucionar()
            print("----------------")
            if sol == []:
                print("No hay solucion")
            else:
                print("¡Se ha solucionado el tablero, asi es como quedo!: ")
                imprimir_tablero(sol)
            print("----------------")
        elif opcion == 4:
            print("----------------")
            print("¡Saliendo del programa!")
            print("----------------")

            break
        else:
            print("----------------")
            print("¡Esa opcion no existe!")
            print("----------------")


if __name__ == "__main__":
    # Intente hacer "python3 main.py hola mundo"
    main()
