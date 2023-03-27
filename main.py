import gamelib
from logica_chess import *


def main():
    gamelib.title("Shape Shifter Chess")
    gamelib.resize(ANCHO_VENTANA, ALTO_VENTANA)

    nivel = 0
    while True:
        respuesta = gamelib.input('¿Desea cargar la última partida? (si/no)')
        if not respuesta or respuesta == 'no':
            nivel = 1
            juego = crear_juego(nivel)
            guardar_partida(juego)
            break
        if respuesta == 'si':
            try:
                juego = cargar_partida(ARCHIVO_GUARDADO)
            except:
                gamelib.say('No hay ninguna partida guardada. ¡Crearemos una nueva!')
                nivel = 1
                juego = crear_juego(nivel)
                guardar_partida(juego)
            break

    tablero, pos_ultima_pieza, ultima_pieza, nivel, cantidad_fichas = juego

    while gamelib.is_alive():
        if cantidad_fichas == 1:
            nivel += 1
            juego = crear_juego(nivel)
            tablero, pos_ultima_pieza, ultima_pieza, nivel, cantidad_fichas = juego
            guardar_partida(juego)

        juego_mostrar(tablero, nivel, pos_ultima_pieza, ultima_pieza)

        ev = gamelib.wait()
        if not ev:
            break

        if ev.type == gamelib.EventType.KeyPress and ev.key == 'Escape':
            break

        if ev.type == gamelib.EventType.KeyPress and ev.key.lower() == 'z':
            juego = cargar_partida(ARCHIVO_GUARDADO)
            tablero, pos_ultima_pieza, ultima_pieza, nivel, cantidad_fichas = juego

        if ev.type == gamelib.EventType.ButtonPress and ev.mouse_button == 1:
            pos_ultima_pieza, ultima_pieza, cantidad_fichas = juego_actualizar(tablero, pos_ultima_pieza, ultima_pieza, ev.x, ev.y, cantidad_fichas)


gamelib.init(main)