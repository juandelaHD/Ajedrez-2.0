from creaciones import *

MOVIMIENTOS = crear_dict_piezas()


class Caballo:
    def __init__(self):
        self.nombre = 'caballo'
        self.imagen_blanca = './caballo_blanco.gif'
        self.imagen_roja = './caballo_rojo.gif'

    def __repr__(self):
        return self.nombre

    def movimientos(self):
        lista_movimientos = MOVIMIENTOS[self.nombre]
        return lista_movimientos


class Alfil:
    def __init__(self):
        self.nombre = 'alfil'
        self.imagen_blanca = './alfil_blanco.gif'
        self.imagen_roja = './alfil_rojo.gif'

    def __repr__(self):
        return self.nombre

    def movimientos(self):
        lista_movimientos = MOVIMIENTOS[self.nombre]
        return lista_movimientos


class Torre:
    def __init__(self):
        self.nombre = 'torre'
        self.imagen_blanca = './torre_blanco.gif'
        self.imagen_roja = './torre_rojo.gif'

    def __repr__(self):
        return self.nombre

    def movimientos(self):
        lista_movimientos = MOVIMIENTOS[self.nombre]
        return lista_movimientos
