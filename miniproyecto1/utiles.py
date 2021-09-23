import numpy as np
from IPython.display import display, Math, Latex


# ======================= [Clase Lista Prioritaria] ==================
class ListaPrioritaria():
    
    def __init__(self):
        self.diccionario = {}
        
    def __str__(self):
        cadena = '['
        inicial = True
        for costo in self.diccionario:
            elementos = self.diccionario[costo]
            for elemento in elementos:
                if inicial:
                    cadena += '(' + str(elemento) + ',' + str(costo) + ')'
                    inicial = False
                else:
                    cadena += ', (' + str(elemento) + ',' + str(costo) + ')'

        return cadena + ']'
    
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

# ======================= [Algoritmos y funciones auxiliares] ==================

def breadth_first_search(problema):
    nodo = Nodo(problema.estado_inicial, None, None,0, problema.codigo(problema.estado_inicial)) # inicializacion
    if problema.test_objetivo(nodo.estado):
        return nodo
    # La frontera comienza con la raiz
    frontera = [nodo]
    explorados = []
    #print("cod:",nodo.codigo)
    #print("===============")
    while len(frontera) > 0:
        # Se selecciona el primer nodo de la frontera
        nodo = frontera.pop(0)
        # print("cod:",nodo.codigo)
        # print("===============")
        explorados.append(nodo.codigo)
        # Se busca todas las acciones posibles con el nodo seleccionado
        acciones = problema.acciones_aplicables(nodo.estado)
        for a in acciones:
            hijo = nodo_hijo(problema, nodo, a)
            # Se prueba si alguno de los hijos es solucion al problema
            if problema.test_objetivo(hijo.estado):
                return hijo
            # de lo contrario se agregan a la frontera para pasar al siguiente nivel
            if hijo.codigo not in explorados:
                frontera.append(hijo)
    return None

def depth_first_search(problema):
    nodo = Nodo(problema.estado_inicial, None, None,0, problema.codigo(problema.estado_inicial)) # inicializacion
    if problema.test_objetivo(nodo.estado):
        return nodo
    frontera = [nodo] # lista LIFO
    explorados = []
    #print("cod:",nodo.codigo)
    #print("===============")
    while len(frontera) > 0:
        nodo = frontera.pop()
        #print("cod:",nodo.codigo)
        # print("===============")
        explorados.append(nodo.codigo)
        acciones = problema.acciones_aplicables(nodo.estado)
        for a in acciones:
            hijo = nodo_hijo(problema, nodo, a)
            if problema.test_objetivo(hijo.estado):
                return hijo
            if hijo.codigo not in explorados:
                frontera.append(hijo)
    return None



def find_path(nodo):
    # Retorna la lista de acciones desde la raiz hasta el nodo recibido
    # nodo: nodo del cual se busca el camino
    if nodo.madre == None:
        return []
    else:
        return find_path(nodo.madre) + [nodo.accion]
def get_codes(nodo):
    # Encuentra el codigo de todos los nodos siguiendo d¿el camino desde la raiz hasta el nodo
    if nodo.madre == None:
        return [nodo.codigo]
    else:
        return get_codes(nodo.madre) + [nodo.codigo]
def is_cycle(nodo):
    # determina si el camino de estados desde la raiz hasta el nodo recibido
    # tiene ciclos
    camino = get_codes(nodo)
    # Si hay codigos repetidos entonces al incluir la lista de codigos en un conjunto
    # los elementos repetidos se van por lo que la longitud cambia
    return len(camino) != len(set(camino))
def depth_limited_search(problema, L):
    # Realiza una busqueda en profundidad limitada
    # retorna el nodo solucion del problema o error o cutoff
    # ARGUMENTOS:
        # problema: problema que se quierer resolver
        # L: limite de profundidad máxima
    nodo = Nodo(problema.estado_inicial, None, None,0, problema.codigo(problema.estado_inicial)) # inicializacion
    frontera = [nodo]
    resultado = None
    while len(frontera) > 0:
        nodo = frontera.pop()
        if problema.test_objetivo(nodo.estado):
            return nodo
        if depth(nodo) >= L:
            resultado = "cutoff"
        elif not is_cycle(nodo):
            frontera += expand(problema, nodo)
    return resultado
    
def expand(problema, n):
    # Proporciona todos los nodos hijo que se obtienen a partir de un nodo madre
    # mediante cada una de las acciones aplicables
    # ARGUMENTOS:
        # problema: problema que se quierer resolver
        # n: Nodo del cual se obtiene la lista de hijos

    s = n.estado
    nodos = [] # Lista LIFO
    for a in problema.acciones_aplicables(s):
        nodos.append(nodo_hijo(problema, n, a))
    return nodos


def depth(nodo):
    # Calcula la profundidad de un nodo
    # ARGUMENTOS:
        # nodo: nodo del arbol de nodos con estados
    if nodo.madre == None:
        return 0
    else:
        return 1 + depth(nodo.madre)
    
def iterative_deepening_search(problema, l_max):
    # Busqueda iterativa profunda
    # ARGUMENTOS:
        # problema: problema que se quiere resolver
        # l_max: profundidad maxima a probar
    for depth in range(l_max+1):
        print("Con profundidad %d ..." %depth)
        resultado = depth_limited_search(problema, depth)
        if resultado != "cutoff":
            return resultado
        print("Terminado!")
        print("-----------")

def best_first_search(problema,f):
    # implementacion de depth first search con funcion de costo

    # ARGUMENTOS:
    # problema: problema el cual se trabaja
    # f: funcion de costo
    
    #Inicializacion
    setattr(problema, "costo", f) # configuracion de funcion de costo para problema
    s = problema.estado_inicial
    cod = problema.codigo(s)
    nodo = Nodo(s, None, None,0, cod) # nodo raiz
    frontera = ListaPrioritaria() # lista prioritaria
    frontera.push(nodo, nodo.costo_camino)
    explorados = {cod:0}
    
    # Iteraciones de busqueda
    while not frontera.is_empty():
        nodo = frontera.pop()
        if problema.test_objetivo(nodo.estado):
            return nodo
        for hijo in expand(problema, nodo):
            # Se busca cada uno de los hijos del nodo actual con estado, codigo y costo hasta hijo
            s = hijo.estado # estado de hijo
            cod = problema.codigo(s) #codigo del estado del hijo
            c = hijo.costo_camino # costo del camino hasta hijo
            # Si el hijo no ha sido explorado o el costo hasta hijo es menor (camino optimo)
            if cod not in explorados.keys() or c < explorados[cod]:
                frontera.push(hijo, c)
                explorados[cod] = c
    return None

# ==================== [Redefinicion de la clase Nodo] ===============================
class Nodo:
    
    # Clase para crear los nodos
    
    def __init__(self, estado, madre, accion, costo_camino, codigo):
        self.estado = estado
        self.madre = madre
        self.accion = accion
        self.costo_camino = costo_camino
        self.codigo = codigo
        

def nodo_hijo(problema, madre, accion):
    
    # Función para crear un nuevo nodo
    # Input: problema, que es un objeto de clase ocho_reinas
    #        madre, que es un nodo,
    #        accion, que es una acción que da lugar al estado del nuevo nodo
    # Output: nodo
    
    estado = problema.transicion(madre.estado, accion)
    try:
        costo_camino = madre.costo_camino + problema.costo(estado=madre.estado, accion=accion)
    except TypeError as e:
        costo_camino = madre.costo_camino + problema.costo(self=problema,estado=madre.estado, accion=accion)
    codigo = problema.codigo(estado)
    
    return Nodo(estado, madre, accion, costo_camino, codigo)

def solucion(n):
    if n.madre == None:
        return []
    else:
        return solucion(n.madre) + [n.accion]
    
    
    
# ==================== [ Funciones Adicionales ] ===============================
def existe(s,idx):
    # s: string del que se quiere validar si existe el caracter
    # idx: indice de iterador
    return idx < len(s)

def toTex(s1:str,s2:str,r:str,S1:str,S2:str,R:str):
    txt = (
        r"\begin{align*}"+"\n"+
        r"\begin{matrix}"+"\n" +
        f"{s1}"+r"&\\"+"\n"+
        f"{s2}"+r"&\\"+"\n"+
        r"\hline&\\"+"\n"+
        f"{r}"+r"&\\"+"\n"+
        r"\end{matrix}"+"\n"+
        r"\to"+"\n"+
        r"\begin{matrix}"+"\n" +
        f"{S1}"+r"&\\"+"\n"+
        f"{S2}"+r"&\\"+"\n"+
        r"\hline&\\"+"\n"+
        f"{R}"+r"&\\"+"\n"+
        r"\end{matrix}"+
        r"\end{align*}"
    )
    display(Latex(txt))

def recSolution(prob,sol:dict):
    s1 = prob.sumandos[0]
    s2 = prob.sumandos[1]
    r  = prob.resultado
    
    S1 = ''.join([str(sol[i]) for i in s1])
    S2 = ''.join([str(sol[i]) for i in s2])
    R  = ''.join([str(sol[i]) for i in  r])
    
    return (s1,s2,r,S1,S2,R)
    