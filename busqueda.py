from typing import List

# ====| C L A S E S |==== #
class Nodo:
    # Clase para crear los nodos

    def __init__(self, estado, madre, accion, costo_camino, codigo):
        self.estado = estado
        self.madre = madre
        self.accion = accion
        self.costo_camino = costo_camino
        self.codigo = codigo


def nodo_hijo(problema, madre: Nodo, accion: int) -> Nodo:

    # Función para crear un nuevo nodo
    # Input: problema, que es un objeto de clase ocho_reinas
    #        madre, que es un nodo,
    #        accion, que es una acción que da lugar al estado del nuevo nodo
    # Output: nodo

    estado = problema.transicion(madre.estado, accion)
    costo_camino = madre.costo_camino + problema.costo(madre.estado, accion)
    codigo = problema.codigo(estado)
    return Nodo(estado, madre, accion, costo_camino, codigo)


# ====| O T R A S |==== #

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

    return False


# N3
def EXPAND(problema, nodo: Nodo) -> List[Nodo]:
    s = nodo.estado
    nodos = list()

    for ac in problema.acciones_aplicables(s):
        hijo = nodo_hijo(problema, nodo, accion)
        nodos.append(hijo)

    return nodos


# ====| B U S Q U E D A |==== #
def depth_limited_search(problema, l:int) -> str:
    pass


