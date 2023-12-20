### Tarea 2 - Vicente Jesús Muñoz Lizama

## Servidor

Para iniciar el servidor, se utiliza el siguiente comando:

```bash
python3 main.py <puerto>
```

### Requerimientos

Dentro de la carpeta del servidor, es necesario que exista un archivo llamado **configuracion.json** con los campos "host" y "nombres_baneados". El primer campo debe contener una cadena de texto que corresponde a la dirección IP o al nombre del host donde se ejecutará el servidor, y el campo "nombres_baneados" debe ser una lista de cadenas de texto que contiene los nombres no permitidos para jugar.

Nota: Se recomienda crear un archivo llamado "puntajes.txt" en la carpeta "util" en caso de que no exista. Esto es importante ya que, debido a problemas de permisos, el programa puede no ser capaz de crearlo.

### Explicación del servidor

0. **main.py**: Este archivo debe ser ejecutado para abrir el servidor.

Dentro de la carpeta "util", se encuentran los siguientes archivos:

1. **datos_guardados.py**
2. **funciones_servidor.py**
3. **peticiones.py**
4. **util.py**

#### datos_guardados.py

La clase "datos" se encarga de interactuar con el archivo **puntajes.txt**. Al inicio, carga todos los usuarios de este archivo y los almacena en una lista de usuarios que contiene instancias de la clase "Usuario". Además, posee el método "obtener_salón_de_la_fama", que permite obtener los 5 usuarios con mayor puntaje a partir de la lista de usuarios. También cuenta con el método "guardar_usuario" para guardar los datos de un usuario, incluyendo cambios de nivel o puntaje.

La clase "Usuario" representa a un usuario y ofrece métodos como "json" para transformar la información del usuario en un formato JSON que es útil para enviarla al cliente. También implementa los métodos "eq", "str" y "repr" para convertirlo en una cadena de texto y permitir el uso de los operadores "==" e "in".

#### funciones_servidor.py y util.py

El archivo "funciones_servidor.py" contiene funciones para encriptar, serializar, separar mensajes, así como para comprobar si el nombre de usuario está en la lista de nombres no permitidos, que se carga a partir del archivo "nombres_baneados" en el archivo **configuracion.json**. Además, incluye funciones para descodificar, desencriptar, deserializar y determinar cuántos fragmentos de 36 partes se necesitan para un valor de longitud ingresado. Por último, se encuentra la función "log" encargada de registrar eventos en el servidor.

El archivo "util" contiene funciones que ayudan a ejecutar las funciones en "funciones_servidor".

#### peticiones.py

Este archivo contiene la clase "JugadorOnline", que hereda de "Thread". La clase cuenta con dos variables estáticas: "guardar" y "datos". "guardar" es un candado (lock) que se utiliza para evitar que se realicen dos operaciones de guardado simultáneas. 

La clase "JugadorOnline" dispone de los siguientes métodos:

1. "_recivir_mensaje": Se ejecuta cuando se recibe un mensaje.
2. "mandar_mensaje_json": Utilizado por el servidor para enviar un mensaje al cliente.
3. "pedir_salón_de_la_fama": Se ejecuta cuando un mensaje contiene el campo "pedir_salón_de_la_fama", y se encarga de enviar los datos de los 5 mejores jugadores.
4. "verificar_nombre": Si un mensaje incluye el campo "nombre", se verifica si ese nombre está permitido y se envía una respuesta al cliente.
5. "guardar_usuario": Si un mensaje contiene el campo "guardar_usuario", se ejecuta para guardar los datos de un usuario, incluyendo su nombre, puntaje y nivel.

Cada función tiene su propio registro de eventos (log).

La clase cuenta con un "recv" que tiene un tiempo de espera de 3 segundos para que, en caso de recibir la señal de desconexión, no se quede bloqueado y permita desconectar al cliente.

#### main.py

El archivo "main.py" se encarga de iniciar el servidor. Carga el archivo JSON y transfiere los nombres no permitidos a cada instancia de "JugadorOnline" que se cree. Además, recibe el argumento "puerto", que determina el puerto en el que se ejecutará el servidor. En caso de utilizar "CTRL+C" para cerrar el servidor, se enviará una señal para desconectar a los clientes y, posteriormente, se cerrará el servidor.

### Cliente

Para iniciar el cliente, se utiliza el siguiente comando:

```bash
python3 main.py <puerto>
```

Requerimientos

Dentro de la carpeta "cliente" debe existir un archivo **configuracion.json** que tenga "host_servidor", que es una cadena con la dirección IP del servidor al que se conectará el juego. Además, debe existir un archivo llamado "parametros.py" que contenga las siguientes variables:

1. ANCHO_LABERINTO = 16
2. LARGO_LABERINTO = 16
   - Determina las dimensiones de los laberintos (solo se probó con 16x16).
3. DURACION_NIVEL_INICIAL: Duración del primer nivel.
4. VELOCIDAD_LOBO: Velocidad del lobo.
5. PONDERADOR_LABERINTO_1
6. PONDERADOR_LABERINTO_2
7. PONDERADOR_LABERINTO_3
   - Ponderación al tiempo que durará el primer nivel y dificultad de los lobos (mientras más pequeño, más difícil).
8. PUNTAJE_LOBO: Puntaje que da el lobo al matar a uno.
9. CANTIDAD_VIDAS: Vidas iniciales.
10. VELOCIDAD_CONEJO: Velocidad del conejo.
11. VELOCIDAD_ZANAHORIA: Velocidad de las zanahorias.
12. TIEMPO_BOMBA: Duración del efecto de la bomba en el mapa.
13. PUNTAJE_INF: Puntaje al usar el truco I+N+F.
14. INTERVALO_DISPARO_CANON: Cada cuánto disparan los cañones (no estaba originalmente, es muy importante agregarlo si no está presente).

Importante: En la carpeta "frontend", debe existir una carpeta "assets" que contenga las siguientes subcarpetas:

1. "laberintos"
   - Debe tener 3 laberintos con los nombres "tablero_1.txt", "tablero_2.txt" y "tablero_3.txt" con el siguiente formato:
   
```
P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,
E,C,-,-,-,-,-,P,BM,-,-,-,-,-,-,P,
P,P,P,P,P,P,-,P,P,P,P,P,P,P,-,P,
P,P,-,-,-,-,-,P,-,-,-,-,P,-,-,P,
P,-,-,P,P,P,P,P,-,P,P,P,P,-,-,P,
P,-,-,-,-,-,-,P,-,-,-,P,-,-,P,P,
P,-,P,-,-,-,-,-,-,-,-,P,P,-,-,P,
P,P,P,P,P,P,P,P,P,P,-,P,CD,-,-,P,
P,-,-,-,-,P,-,-,-,-,-,P,-,-,-,P,
P,-,-,-,-,P,-,-,P,P,P,P,-,-,P,P,
P,-,-,P,-,P,-,-,-,-,-,P,-,-,-,P,
P,P,-,-,-,P,P,LV,-,P,-,-,-,-,-,P,
P,-,-,-,-,P,-,-,-,-,P,-,-,-,-,P,
P,-,P,P,-,-,-,-,-,-,-,-,-,-,-,P,
P,-,-,P,-,P,-,-,P,-,-,-,-,P,-,P,
P,P,S,P,P,P,P,P,P,P,P,P,P,P,P,P,
```

   - Deben tener dimensiones de ANCHO_LABERINTO * LARGO_LABERINTO y, según el enunciado, son de 16x16. No olvidarse de las comas, ya que de lo contrario podrían generarse errores.

2. "sonidos"
   - Contiene los sonidos "derrota.wav" y "victoria.wav". Es muy importante que sean archivos **.wav**, ya que los sonidos utilizan una clase incompatible con otros formatos.

3. "sprites"
   - Deben ser sprites con los mismos nombres que se mencionan en el enunciado y, si es posible, con la misma resolución.

**Otra cosa importante seria ejecutarlo en WSL pues al probar en Windows se demoraba en iniciar los niveles (20 segundos)**


Frontend

La carpeta "frontend" se compone de 3 carpetas: "views", donde se encuentran las ventanas que se mostrarán; "components", donde están los componentes que se reutilizan en varias partes de las vistas; y la carpeta mencionada en los requerimientos, "assets".

Carpeta Components

La carpeta "components" contiene los siguientes archivos:

1. components.py
2. informacion.py
3. juego.py
4. sonidos.py

- "components.py":
   - Contiene los siguientes componentes:
     1. DCClogo: para poner el logo del juego.
     2. Sprite: se encarga de mostrar las imágenes de cada celda, con una lista de entidades (como conejo, bomba, item) y un fondo que puede ser celda vacía o muro. También tiene el evento "poner item" para detectar en qué celda el jugador presionó para poner el item.
     3. ItemInventario: muestra el item en el inventario, además de eventos de apretar y el método "__eq__" para que funcionen los operadores "==" e "in".
     4. Mensaje: muestra un texto con un color y tamaño de letra.
     5. Botones: sirve para crear varios botones a la vez.
     6. Entrada de texto: permite ingresar texto.

- "informacion.py":
   - Aquí se encuentra el componente "Información", que muestra el tiempo, vidas, puntaje, nivel e inventario, además de botones para pausar o salir del juego. Tiene los métodos para actualizar el nivel, los segundos, el puntaje, las vidas y el inventario, así como para cambiar el mensaje al poner un item. También contiene una instancia de "Inventario", que es el backend que maneja el inventario.

- "juego.py":
   - Este componente muestra el juego, crea el grid donde se verán los sprites (las celdas del juego), detecta las teclas presionadas y los trucos. Además, tiene un método para renderizar el laberinto en pantalla y una instancia de "Mundo", que es el backend que maneja el juego.

- "sonidos.py":
   - Aquí se encuentran las clases para reproducir los sonidos correspondientes, como "SonidoPerder" y "SonidoGanar".

Carpeta Views

La carpeta "views" contiene las ventanas que se mostrarán durante el juego:

1. "FinJuego.py":
   - Muestra si ganaste o perdiste, o si se perdió la conexión con el servidor.

2. "JuegoWindow.py":
   - Muestra el juego y contiene los componentes "Informacion" y "Juego". Escucha la tecla "ESC" para salir de la aplicación y tiene métodos para cargar el nivel correspondiente y para ocultar la ventana. Aquí se configuran los eventos entre "Juego" y "Informacion" para que estén coordinados.

3. "MainWindow.py":
   - Muestra la entrada de texto del nombre y el salón de la fama.

Backend

El backend se encarga de toda la lógica del juego y la carpeta contiene:

1. "entidades":
   - Contiene "entidades.py", que tiene la lógica de todas las entidades del juego. Esto es el núcleo del juego, ya que todas las interacciones con otras entidades se realizan gracias a esto. Las clases de entidades son:

     1. Entidad
     2. EntidadMovimiento
     3. ConejoChico
     4. Lobo
     5. LoboHorizontal
     6. LoboVertical
     7. Zanahoria
     8. Canon
     9. Item
     10. BombaManzana
     11. BombaCongelacion
     12. Efectos
     13. Explosion
     14. Congelacion

   - Esto se creó para evitar repetir código y permitir que todo fuera más fácil respecto a las interacciones.

2. "inventario":
   - Contiene "inventario.py", que es la clase del backend que maneja la interacción con el componente "Informacion" para saber qué item se tiene seleccionado y detectar si se puede poner o no.

3. "mundo":
   - Contiene "mundo.py", que es la clase "Mundo", la cual maneja toda la lógica del juego. Algunos de los métodos clave son:

     - "cambio_duracion": gestiona el cambio de la duración del nivel y actualiza el puntaje del jugador.
     - "cambio_vida": maneja el cambio en la vida de un personaje del juego.
     - "cargar_laberinto": carga un nuevo laberinto y configura los elementos del juego según el nivel actual.
     - "mover": gestiona el movimiento de los personajes en el juego y las interacciones.
     - "aparecer_zanahoria": hace aparecer zanahorias en el juego cuando un cañón dispara.
     - "coger_item": controla la interacción del "Conejo Chico" al recoger un objeto.
     - "alternar_pausa": alterna entre pausa y juego en tiempo real.
     - "borrar_villanos": elimina a los villanos del juego.
     - "infinito": activa el modo "infinito" en el que el "Conejo Chico" es inmortal.
     - "lanzar_evento_poner_item": lanza un evento para colocar un ítem en una casilla específica del juego.
     - "usar_item": permite que el "Conejo Chico" use un ítem.
     - "agregar_efecto": agrega efectos especiales en el juego cuando se usa un ítem.
     - "vida_conejo": restaura la vida del "Conejo Chico" al valor máximo permitido para el nivel actual.

4. "net":
   - En esta carpeta se encuentra "cliente.py", que se encarga de la conexión con el servidor, "funciones_servidor" que contiene las funciones para encriptar y desencriptar, y "util" que son funciones utilizadas por "funciones_servidor".

5. "procesador":
   - Contiene "procesador.py", que tiene la clase "Procesador" encargada de controlar la interacción con el servidor y enviar eventos para iniciar el juego si el servidor confirma que el nombre es válido.

6. funciones_cliente: 

    - Contiene funciones para calcular el puntaje, validación de formato y obtención de laberintos por nivel.

### Implementación:

Mecánicas:
Los laberintos se cargan en la clase Mundo con la ayuda de la función "obtener_laberinto_nivel". Luego, hay un proceso en el que cada celda se convierte en un sprite con su respectivo fondo y las entidades que contiene.

Niveles, dificultad:
El nivel se carga desde el servidor con la clase "Procesador" y se pasa a "Juego" cargando el nivel correcto. En la clase Mundo, al cargar el laberinto, se calcula la velocidad del lobo y la duración del nivel, y se envía al componente Información. Esta implementación se encuentra en la clase Mundo, en el método "cambio_duracion".

Puntaje:
El puntaje se recalcula cada segundo hasta que se termine el nivel, momento en el que pasa a ser un puntaje base. Por lo tanto, en la partida se muestra el puntaje total en el juego, no el que se lleva durante el nivel. Esta lógica se encuentra en la clase Mundo, en la función "cambio_duracion".

Fin de nivel:
El fin de nivel está implementado en la Clase Mundo, en el método "mover".

Fin del juego:
El fin del juego está implementado en la clase Mundo, en la función "cambio_vida".

Entidades:
Todas las entidades están modeladas en "entidades.py" y su interacción con las demás se verifica en la clase Mundo, en los métodos "aparecer_zanahoria", "mover" y "coger_item".

Interacción:
La interacción entre las entidades se modela en "entidades.py" con las animaciones, las cuales se reproducen en la clase Mundo en el método "mover".

El clic para los items se verifica en la clase Mundo con el método "lanzar_evento_poner_item", que es escuchado por "Informacion.inventario_clase.poner_item". En caso de que sea posible ponerlo, se lanza el evento "evento_usar_item", el cual es escuchado por "self.juego.mundo.usar_item".

Cheatcode:
Los trucos están implementados en el componente Juego.

Interfaz gráfica:
La interfaz gráfica está implementada en la carpeta "views".

Networking:
La implementación de la red está en la carpeta "servidor", además de la codificación y el uso de JSON.

Logs:
Los registros están implementados con la función "log" del servidor.

Sonido:
Los sonidos están implementados en "FinJuego" en "Views".

#### Entrega Final: 46 pts (75%)
##### ✅ Ventana Inicio
##### ✅ Ventana Juego
##### ✅ ConejoChico
##### ✅ Lobos
##### ✅ Cañón de Zanahorias
##### ✅ Bomba Manzana
##### ✅ Bomba Congeladora
##### ✅ Fin del nivel
##### ✅ Fin del Juego
##### ✅ Recoger (G)
##### ✅ Cheatcodes (Pausa, K+I+L, I+N+F)
##### ✅ Networking
##### ✅ Decodificación
##### ✅ Desencriptación
##### ✅ Archivos
##### ✅ Funciones

### Información importante:
La función "funciones_servidor" de la entrega intermedia se utilizó por completo para encriptar y desencriptar. Sin embargo, al crear las entidades y el Mundo que se comunican con eventos, "funciones_cliente.py" no resultó muy útil. Solo se utilizó "validacion_formato", "calcular_puntaje" y se agregó la función "obtener_laberinto_nivel". Las funciones "riesgo_mortal" no resultaron útiles, ya que al moverse con el método "interaccion" de la clase Entidad se comprobaba si se perdía una vida, lo que hacía inútil la función. "Usar_item" tampoco fue necesario, ya que el inventario, como lista, está en ConejoChico y al usarlo no se necesita una verificación de True o False, ya que esta verificación ocurre antes en Información. La función "validar_direccion" tampoco fue necesaria, ya que las entidades siempre envían el evento de movimiento y el Mundo solo se encarga de verificar si es válido, por lo que no necesita verificar la tecla.