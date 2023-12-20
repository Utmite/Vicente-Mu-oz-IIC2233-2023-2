# Tarea 1: DCChexxploding :school_satchel:
---
Para ejecutar la tarea debes poner el la terminal:
```bash
cd /carpeta_tarea
python3 main.py <tu nombre> <nombre tablero>
```
**IMPORTANTE**: En la carpeta del main debe existir un tableros.txt para poder cargar el tablero!
---
### Cosas implementadas y no implementadas :white_check_mark: :x:

* Parte 1 - Funcionalidades
    * PiezaExplosiva: 
        - verificar_alcance: Completo :white_check_mark:
    * Tablero:
        - desglose :white_check_mark:
        - peones_invalidos :white_check_mark:
        - piezas_explosivas_invalidas  :white_check_mark:
        - tablero_transformado :white_check_mark:
        - celdas_afectadas :white_check_mark:
        - limpiar :white_check_mark:
        - reemplazar :white_check_mark:
        - solucionar :white_check_mark:
*  Parte 2 - Menú
    - Acciones: Completo :white_check_mark:
---
### Librerías externas utilizadas

1. ```os```: ```path```
2. ```copy```: ```deepcopy()```

### Librerías propias utilizadas

1. ```NotTablero```: ```NotTablero```

Es una copia de tablero pues necesitaba una clase que hiciera lo mismo pero me daba error instanciar
tablero adentro de tablero en solucionar


