class Jugador():
    ''' Modela la entidad jugador. Dispondrá de nombre y puntuación parcial (para cada partida) y total.
    Deberá guardarse en fichero para no perderlos.
    '''

    def __init__(self, nom, res=0, total=0, id_tabla=0) -> None:
        ''' Constructor de la clase. Inicializa el jugador y si ya existe lo lee de la BD
        '''
        self.__nombre = nom
        self.__resultado = res          # para guardar el tanteo de la partida actual
        self.__total_puntos = total
        self.__id_tabla = id_tabla

    @property
    def id(self):
        return self.__id_tabla
    
    @property
    def nombre(self):
        return self.__nombre
    @nombre.setter
    def nombre(self, nom):
        self.__nombre = nom

    @property
    def resultado(self):
        return self.__resultado
    @resultado.setter
    def resultado(self, res):
        self.__resultado = res
    
    @property
    def total_puntos(self):
        return self.__total_puntos
    @total_puntos.setter
    def total_puntos(self, total):
        self.__total_puntos = total

    
    def __str__(self) -> str:
        salida = 'Jugador: {0}  (Total puntos: {1})'
        return salida.format(self.__nombre, self.__total_puntos)
    