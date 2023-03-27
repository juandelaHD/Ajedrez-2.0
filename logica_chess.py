from random import choice
from creaciones import *
from piezas import *
import gamelib

# tablero de 360x360 ---> dimensión de CASILLA 45x45 (tablero de 8x8)
ANCHO_VENTANA, ALTO_VENTANA = 400, 460
Px, Py = 20, 50
DIMENSION_CASILLA = 45

ARCHIVO_GUARDADO = 'Shape_Shifter_Chess.txt'
PIEZAS = [Caballo(), Torre(), Alfil()]

COLORES = ('red', 'white')
BORDE_FICHAS = 'blue'

def es_movimiento_valido(x, y):
    """Devuelve un booleando dependiendo que los parametros x e y estén dentro de las dimensiones del tablero"""
    return (0 <= x < CANT_COLUMNAS) and (0 <= y < CANT_FILAS)


def crear_juego(n_nivel):
    """Inicializa el estado del juego para el numero de nivel dado"""
    cantidad_fichas = n_nivel + 2
    tablero = crear_tablero_vacio()

    pieza_actual = choice(PIEZAS)
    pos_i_pieza, pos_j_pieza = (choice(range(CANT_FILAS)), choice(range(CANT_COLUMNAS)))

    for i in range(cantidad_fichas):
        
        lista_direcciones = []
        for direccion in pieza_actual.movimientos():
            x, y = pos_i_pieza + direccion[0], pos_j_pieza + direccion[1]
            lista_direcciones.append((x, y))
        
        posible_posicion = choice(lista_direcciones)
        x, y = posible_posicion[0], posible_posicion[1]
        while not es_movimiento_valido(x, y) or tablero[x][y] != ' ':
            lista_direcciones.remove(posible_posicion)
            posible_posicion = choice(lista_direcciones)
            x, y = posible_posicion[0], posible_posicion[1]

        tablero[x][y] = pieza_actual
        if i == n_nivel+1:
            pos_ultima_pieza = x, y
            ultima_pieza = pieza_actual
            continue
        pieza_actual = choice(PIEZAS)
        pos_i_pieza, pos_j_pieza = x, y

    juego = [tablero,  pos_ultima_pieza,
             ultima_pieza, n_nivel, cantidad_fichas]
    return juego


def evaluar_posibles_movimientos(pieza, pos_i_pieza, pos_j_pieza):
    """Devuelve una lista con todas las posiciones donde se puede mover una determinada pieza"""
    posibles_casilleros = []
    for direccion in pieza.movimientos():
        posible_casillero = (pos_j_pieza + direccion[1], pos_i_pieza + direccion[0])
        if es_movimiento_valido(posible_casillero[0], posible_casillero[1]):
            posibles_casilleros.append(posible_casillero)
    return posibles_casilleros


def juego_actualizar(tablero, pos_ultima_pieza, ultima_pieza, x, y, cantidad_fichas):
    """Actualizar el estado del juego

    x e y son las coordenadas (en pixels) donde el usuario hizo click.
    Esta función determina si esas coordenadas corresponden a una celda
    del tablero; en ese caso determina el nuevo estado del juego y lo
    devuelve.
    """
    pos_i_click = (y-Py)//DIMENSION_CASILLA
    pos_j_click = (x-Px)//DIMENSION_CASILLA
    posicion_click = ((y-Py)//DIMENSION_CASILLA, (x-Px)//DIMENSION_CASILLA)

    posibles_movimientos = evaluar_posibles_movimientos(
        ultima_pieza, pos_ultima_pieza[0], pos_ultima_pieza[1])

    if posicion_click in posibles_movimientos and tablero[pos_j_click][pos_i_click] != ' ':
        tablero[pos_ultima_pieza[0]][pos_ultima_pieza[1]] = ' '
        ultima_pieza = tablero[posicion_click[1]][posicion_click[0]]
        pos_ultima_pieza = (posicion_click[1], posicion_click[0])
        cantidad_fichas -= 1

    return pos_ultima_pieza, ultima_pieza, cantidad_fichas


def cargar_partida(archivo):
    """Devuelve el juego que se haya guardado en un determinado archivo.txt"""
    with open(archivo) as f:
        contador = 1
        tablero = crear_tablero_vacio()

        for linea in f:
            linea = linea.rstrip()
            fila = (contador-1) // 8
            columna = (contador-1) % 8
            if linea == Caballo().nombre:
                tablero[fila][columna] = Caballo()
            if linea == Alfil().nombre:
                tablero[fila][columna] = Alfil()
            if linea == Torre().nombre:
                tablero[fila][columna] = Torre()
            if contador == 65:
                aux = linea.split(", ")
                pos_ultima_pieza = (int(aux[1]), int(aux[0]))
            elif contador == 66:
                n_nivel = int(linea)
                cantidad_fichas = n_nivel + 2
            contador += 1
        ultima_pieza = tablero[pos_ultima_pieza[0]][pos_ultima_pieza[1]]
        juego = [tablero, pos_ultima_pieza,
                 ultima_pieza, n_nivel, cantidad_fichas]
        return juego


def guardar_partida(juego):
    """Guarda la primera instancia del juego creado en un archivo.txt"""
    with open(ARCHIVO_GUARDADO, 'w') as f:
        for i in juego[0]:
            for j in i:
                f.write(f'{j}\n')
        f.write(f'{juego[1][1]}, {juego[1][0]}')
        f.write('\n')
        f.write(f'{juego[3]}\n')

def juego_mostrar(tablero, nivel, pos_ultima_pieza, ultima_pieza):
    '''Dibuja la interfaz de la aplicación en la ventana'''
    contador = 0
    posibles_movimientos = evaluar_posibles_movimientos(ultima_pieza, pos_ultima_pieza[0], pos_ultima_pieza[1])

    gamelib.draw_begin()
    gamelib.draw_text('Shape Shifter Chess', ANCHO_VENTANA//2, 25)
    gamelib.draw_text(f'Nivel: {nivel}', ANCHO_VENTANA-340, ALTO_VENTANA-25)
    gamelib.draw_text(f'Salir: Esc', ANCHO_VENTANA-60, ALTO_VENTANA-25)
    gamelib.draw_text(f'Reintentar: Z', ANCHO_VENTANA//2, ALTO_VENTANA-25)

    for i in range(1, ANCHO_VENTANA-(Px*2), DIMENSION_CASILLA):
        contador += 1
        for j in range(1, ALTO_VENTANA-(Py*2), DIMENSION_CASILLA):
            contador += 1
            gamelib.draw_rectangle(Px+i, Py+j, Px+DIMENSION_CASILLA+i, Py+DIMENSION_CASILLA+j, outline='black', width=2, fill=COLORES[contador % 2])

    for i in range(CANT_FILAS):
        for j in range(CANT_COLUMNAS):
            if tablero[i][j] != ' ':
                pieza = tablero[i][j]
                if i == pos_ultima_pieza[0] and j == pos_ultima_pieza[1]:
                    gamelib.draw_image(pieza.imagen_roja, (DIMENSION_CASILLA*i)+Px, (DIMENSION_CASILLA*j)+Py)
                else:
                    gamelib.draw_image(pieza.imagen_blanca, (DIMENSION_CASILLA*i)+Px, (DIMENSION_CASILLA*j)+Py)

    for tupla in posibles_movimientos:
        if tablero[tupla[1]][tupla[0]] != ' ':
            gamelib.draw_rectangle(tupla[1]*DIMENSION_CASILLA+Px, tupla[0]*DIMENSION_CASILLA+Py, tupla[1]*DIMENSION_CASILLA+Px+DIMENSION_CASILLA, tupla[0]*DIMENSION_CASILLA+Py+DIMENSION_CASILLA, outline=BORDE_FICHAS, width=3, fill=None)

    gamelib.draw_end()