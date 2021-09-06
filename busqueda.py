# ====| S E T U P |==== #
import numpy as np
from typing import List, Tuple

# ====| C L A S E S |==== #
class Nodo:
    """Clase para crear los nodos"""

    def __init__(self, estado, madre, accion, costo_camino, codigo):
        self.estado = estado
        self.madre = madre
        self.accion = accion
        self.costo_camino = costo_camino
        self.codigo = codigo


class ListaPrioritaria:
    def __init__(self):
        self.diccionario = {}

    def __str__(self):
        cadena = "["
        inicial = True
        for costo in self.diccionario:
            elementos = self.diccionario[costo]
            for elemento in elementos:
                if inicial:
                    cadena += "(" + str(elemento) + "," + str(costo) + ")"
                    inicial = False
                else:
                    cadena += ", (" + str(elemento) + "," + str(costo) + ")"

        return cadena + "]"

    def push(self, elemento, costo):
        try:
            self.diccionario[costo].append(elemento)
        except:
            self.diccionario[costo] = [elemento]

    def pop(self):
        min_costo = np.min(np.array(list(self.diccionario.keys())))
        candidatos = self.diccionario[min_costo]
        elemento = candidatos.pop()
        if len(candidatos) == 0:
            del self.diccionario[min_costo]
        return elemento

    def is_empty(self):
        return len(self.diccionario) == 0


# ====| O T R A S |==== #


# N3
def nodo_hijo(problema, madre, accion):

    # Función para crear un nuevo nodo
    # Input: problema, que es un objeto de clase ocho_reinas
    #        madre, que es un nodo,
    #        accion, que es una acción que da lugar al estado del nuevo nodo
    # Output: nodo

    estado = problema.transicion(madre.estado, accion)
    try:
        costo_camino = madre.costo_camino + problema.costo(
            estado=madre.estado, accion=accion
        )
    except TypeError as e:
        costo_camino = madre.costo_camino + problema.costo(
            self=problema, estado=madre.estado, accion=accion
        )
        # raise e

    codigo = problema.codigo(estado)
    return Nodo(estado, madre, accion, costo_camino, codigo)


# N3
def solucion(n):
    if n.madre == None:
        return []
    else:
        return solucion(n.madre) + [n.accion]


# N3
def depth(nodo: Nodo) -> int:
    if nodo.madre == None:
        return 0

    else:
        return depth(nodo.madre) + 1


# N3
def is_cycle(nodo: Nodo) -> bool:
    counter = 0
    path = set()
    while nodo != None:
        counter += 1
        path.add(nodo.codigo)

        if counter > len(path):
            return True
        else:
            nodo = nodo.madre

    return None


# N3
def EXPAND(problema, nodo: Nodo) -> List[Nodo]:
    s = nodo.estado
    nodos = list()

    for accion in problema.acciones_aplicables(s):
        hijo = nodo_hijo(problema, nodo, accion)
        nodos.append(hijo)

    return nodos


# N3
def cod_lab(cod: str) -> tuple:
    try:
        temp = cod.split("-")
        return tuple([int(c) for c in temp])
    except AttributeError:
        return cod


# N3
def lab_states(nodo: Nodo) -> List[Tuple[int, int]]:
    estados = list()
    while True:
        if nodo is None:
            break
        estados = [cod_lab(nodo.codigo)] + estados
        nodo = nodo.madre

    return estados


# ====| B U S Q U E D A |==== #

# N2
def depth_first_search(problema):
    nodo = Nodo(problema.estado_inicial, None, None, 0, problema.estado_inicial)

    if problema.test_objetivo(nodo.estado):
        return nodo

    frontera = [nodo]
    explorados = []

    while len(frontera) != 0:
        nodo = frontera.pop()
        explorados.append(nodo.codigo)

        for accion in problema.acciones_aplicables(nodo.estado):
            hijo = nodo_hijo(problema, nodo, accion)

            if problema.test_objetivo(hijo.estado):
                return hijo

            if hijo.codigo not in explorados:
                frontera.append(hijo)

    return None


# N2
def breadth_first_search(problema):
    nodo = Nodo(problema.estado_inicial, None, None, 0, problema.estado_inicial)
    if problema.test_objetivo(nodo.estado):
        return nodo
    frontera = [nodo]
    explorados = []
    while len(frontera) != 0:
        nodo = frontera[0]
        del frontera[0]

        explorados.append(nodo.codigo)
        for accion in problema.acciones_aplicables(nodo.estado):
            hijo = nodo_hijo(problema, nodo, accion)

            if problema.test_objetivo(hijo.estado):
                return hijo

            if hijo.codigo not in explorados:
                frontera.append(hijo)
    return None


# N3
def depth_limited_search(problema, l: int):
    nodo = Nodo(problema.estado_inicial, None, None, 0, problema.estado_inicial)
    frontera = [nodo]
    resultado = None

    while len(frontera) != 0:
        nodo = frontera.pop()

        if problema.test_objetivo(nodo.estado):
            return nodo

        if depth(nodo) >= l:
            resultado = "cutoff"

        elif not is_cycle(nodo):
            frontera += EXPAND(problema, nodo)

    return resultado


# N3
def iterative_deepening_search(problema, l_max: int):
    for depth in range(l_max):
        print(f"Buscando en el nivel {depth}")
        resultado = depth_limited_search(problema, depth)
        if resultado != "cutoff":
            return resultado


# N3
def best_first_search(problema, f=None):
    if f is not None:
        setattr(problema, "costo", f)

    s = problema.estado_inicial
    cod = problema.codigo(s)

    nodo = Nodo(s, None, None, 0, cod)
    frontera = ListaPrioritaria()
    frontera.push(nodo, 0)
    explorados = {}
    explorados[cod] = 0

    while not frontera.is_empty():
        nodo = frontera.pop()

        if problema.test_objetivo(nodo.estado):
            return nodo

        for hijo in EXPAND(problema, nodo):
            s = hijo.estado
            cod = problema.codigo(s)
            c = hijo.costo_camino

            if (cod not in explorados.keys()) or (c < explorados[cod]):
                frontera.push(hijo, c)
                explorados[cod] = c

    return None

# N5
def minimax_search(juego:Juego, estado):
    jugador = juego.a_jugar(estado)
    valor, movimiento = max_value(juego,estado, jugador)
    return movimiento

# N5
def max_value(juego:Juego, estado,jugador):
    if juego.es_terminal(estado):
        return (juego.utilidad(estado,jugador),None)
    v = -inf
    for a in juego.acciones(estado):
        v2,va = min_value(juego,juego.resultado(estado,a),jugador)
        if v2 > v:
            v,movimiento = v2,a
    return (v,movimiento)

# N5
def min_value(juego:Juego, estado, jugador):
    if juego.es_terminal(estado):
        return (juego.utilidad(estado,jugador), None)
    v = inf
    for a in juego.acciones(estado):
        v2,a2 = max_value(juego,juego.resultado(estado,a), jugador)
        if v2 < v:
            v,movimiento = v2,a
    return v, movimiento
