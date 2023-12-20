def usuario_permitido(nombre: str, usuarios_no_permitidos: list[str]) -> bool:
    return nombre not in usuarios_no_permitidos


def serializar_mensaje(mensaje: str) -> bytearray:
    return bytearray(mensaje.encode(encoding="UTF-8"))


def separar_mensaje(mensaje: bytearray) -> list[bytearray]:
    a = bytearray()
    b = bytearray()
    c = bytearray()
    todas = [a, b, c]
    for i, byte in enumerate(mensaje):
        if i != 0 and i % 3 == 0:
            todas = todas[::-1]
        todas[i % 3].append(byte)

    return [a, b, c]


def encriptar_mensaje(mensaje: bytearray) -> bytearray:
    a, b, c = separar_mensaje(mensaje)
    condicion = a[0] + b[-1] + c[0]

    if condicion % 2 == 0:
        resultado = bytearray(b"1") + a + c + b
    else:
        resultado = bytearray(b"0") + b + a + c
    return resultado


def codificar_mensaje(mensaje: bytearray) -> list[bytearray]:
    largo = len(mensaje)
    largo = largo.to_bytes(4, "big")

    chunks = []
    resultado = []
    resultado.append(bytearray(largo))

    for i in range(0, len(mensaje), 36):
        chunk = mensaje[i : i + 36]

        while len(chunk) < 36:
            chunk.append(0)

        chunks.append(bytearray(chunk))

    for i, chunk in enumerate(chunks, 1):
        numero_bloque = i.to_bytes(4, "big")
        resultado.append(bytearray(numero_bloque))
        resultado.append(chunk)

    return resultado
