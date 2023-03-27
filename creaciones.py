import csv

CANT_FILAS = 8
CANT_COLUMNAS = 8


def crear_dict_piezas():
    """Devuelve un diccionario con los posibles movimientos de cada tipo de pieza"""
    movimientos = {}
    with open('movimientos.csv') as f:
        for pieza, mov, extensible in csv.reader(f):
            lista_direcciones = mov.split(';')
            movimientos[pieza] = movimientos.get(pieza, [])
            if extensible == 'true':
                for i in range(1, CANT_COLUMNAS+1):
                    direccion = (int(lista_direcciones[0])*i,int(lista_direcciones[1])*i)
                    movimientos[pieza].append(direccion)
            if extensible == 'false':
                movimientos[pieza].append((int(lista_direcciones[0]),int(lista_direcciones[1])))
    return movimientos


def crear_lista_vacia():
    """Crea una lista con la cantidad máxima de valores posibles según la cantidad de filas y columnas2"""
    lista_vacia = []
    for _ in range(CANT_FILAS*CANT_COLUMNAS):
        lista_vacia.append(' ')
    return lista_vacia


def crear_tablero_vacio():
    tablero = []
    huecos = crear_lista_vacia()
    indice = 0
    for _ in range(CANT_FILAS):
        filas = []
        for _ in range(CANT_COLUMNAS):
            filas.append(huecos[indice])
            indice += 1
        tablero.append(filas)
    return tablero