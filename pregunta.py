import respuesta

class Pregunta():

    def __init__(self, id, cuerpo, tema=1, dific=1, lista_obj_resp=[]) -> None:
        self.__id = id
        self.__cuerpo = cuerpo      
        self.__dificultad = dific                    # obj dificultad
        self.__tematica = tema                       # obj tematica
        self.__l_obj_respuestas = lista_obj_resp     # lista de objetos Respuesta
    
    @property
    def id(self):
        return self.__id

    @property
    def cuerpo(self):
        return self.__cuerpo

    @property
    def dificultad(self):
        return self.__dificultad

    @property
    def tematica(self):
        return self.__tematica

    @property
    def l_obj_respuestas(self):
        return self.__l_obj_respuestas
