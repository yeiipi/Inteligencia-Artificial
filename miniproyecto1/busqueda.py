class Criptoaritmetica:
    """
    Problema de criptoaritmetica, el cual consiste en encontrar
    el valor de todas las letras que aparecen en una operación de suma criptoaritmetica
    """
    def __init__(self,sumando1:str,sumando2:str,resultado:str):
        alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        # inicializacion
        self.solucion = dict()
        self.sumandos = [sumando1.upper(), sumando2.upper()]
        self.resultado = resultado.upper()

        for c in self.sumandos[0]:
            assert c in alfabeto, "ERROR: Algun caracter del primer sumando no esta en el alfabeto"
        for c in self.sumandos[1]:
            assert c in alfabeto, "ERROR: Algun caracter del segundo sumando no esta en el alfabeto"
        for c in self.resultado:
            assert c in alfabeto, "ERROR: Algun caracter del resultado no esta en el alfabeto"

        print(f"Operacion final: {self.sumandos[0]}+{self.sumandos[1]}={self.resultado}")

        # Representacion del estado inicial por medio de un diccionario con valroes iniciales
        # NOTA: cada estado es un diccionario con los siguientes atributos
        self.estado_inicial = {"solucion":dict(),
                               "DigitosNoAsignados":[i for i in range(0,10)],
                               "col": 0,
                               "acarreo":0
                              }class Criptoaritmetica:
    """
    Problema de criptoaritmetica, el cual consiste en encontrar
    el valor de todas las letras que aparecen en una operación de suma criptoaritmetica
    """
    def __init__(self,sumando1:str,sumando2:str,resultado:str):
        alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        # inicializacion
        self.solucion = dict()
        self.sumandos = [sumando1.upper(), sumando2.upper()]
        self.resultado = resultado.upper()

        for c in self.sumandos[0]:
            assert c in alfabeto, "ERROR: Algun caracter del primer sumando no esta en el alfabeto"
        for c in self.sumandos[1]:
            assert c in alfabeto, "ERROR: Algun caracter del segundo sumando no esta en el alfabeto"
        for c in self.resultado:
            assert c in alfabeto, "ERROR: Algun caracter del resultado no esta en el alfabeto"

        print(f"Operacion final: {self.sumandos[0]}+{self.sumandos[1]}={self.resultado}")

        # Representacion del estado inicial por medio de un diccionario con valroes iniciales
        # NOTA: cada estado es un diccionario con los siguientes atributos
        self.estado_inicial = {"solucion":dict(),
                               "DigitosNoAsignados":[i for i in range(0,10)],
                               "col": 0,
                               "acarreo":0
