class Respuesta():
    # Las respuestas no se editan. Se cogen de la base de datos
    
    def __init__(self, id, cuerpo, correcta=False) -> None:
        self.__id = id
        self.__cuerpo = cuerpo
        self.__correcta = correcta

    @property
    def id(self):
        return self.__id
   
    @property
    def cuerpo(self):
        return self.__cuerpo
        
    @property
    def correcta(self):
        return self.__correcta
    