class Modo():
    ''' Modela los parámetros de la partida. Num jugadores, num preguntas y tiempos
    '''
    def __init__(self, 
                tmax_ju=60, 
                tmax_preg=5, 
                num_preg=10, 
                num_jug=1) -> None:
                
        self.__tmax_juego = tmax_ju
        self.__tmax_pregunta = tmax_preg
        self.__num_preguntas = num_preg
        self.__num_jugadores = num_jug

    @property
    def tmax_juego(self):
        return self.__tmax_juego
    @tmax_juego.setter
    def tmax_juego(self, t):
        self.__tmax_juego = t

    @property
    def tmax_pregunta(self):
        return self.__tmax_pregunta
    @tmax_pregunta.setter
    def tmax_pregunta(self, t):
        self.__tmax_pregunta = t

    @property
    def num_preguntas(self):
        return self.__num_preguntas
    @num_preguntas.setter
    def num_preguntas(self, np):
        self.__num_preguntas = np

    @property
    def num_jugadores(self):
        return self.__num_jugadores
    @num_jugadores.setter
    def num_jugadores(self, nj):
        self.__num_jugadores = nj
    
