import os

class Partida():

    def __init__(self,
                dic_obj_jugador,         # podrá haber más de un jugador en la partida
                obj_modo,                   # obj con los sttings del juego actual
                list_obj_preguntas_resp) -> None:
        
        self.__jugadores = dic_obj_jugador              # nos saltamos la validación
        self.__modo = obj_modo
        self.__col_preguntas = list_obj_preguntas_resp
        self.__marcadores = self.__inicializar_marcadores()   # dic de los marcadores de la partida actual

    @property
    def jugadores(self):
        return self.__jugadores
    @jugadores.setter
    def jugadores(self, dic):
        self.__jugadores = dic
        self.__marcadores = self.__inicializar_marcadores()

    @property
    def modo(self):
        return self.__modo

    @property
    def preguntas(self):
        return self.__col_preguntas
    @preguntas.setter
    def preguntas(self, lista):
        self.__col_preguntas = lista

    @property
    def marcadores(self):
        return self.__marcadores
    @marcadores.setter
    def marcadores(self, dic_new_marc):
        self.__marcadores = dic_new_marc
    
    def __inicializar_marcadores(self):
        dic_new_marcador = {}
        for jug in self.__jugadores.values():
            dic_new_marcador[jug.nombre] = 0
        return dic_new_marcador

    def iniciar(self, modo):
        self.__jugadores = {}
        self.__modo = modo
        self.__col_preguntas = []
        self.__marcadores = self.__inicializar_marcadores()
        #print(self.__col_preguntas[0].respuestas)

    def __str__(self) -> str:
        print(f'nombre: {self.__jugadores} con marcadores: {self.__marcadores}')

    def mostrar_info_partida(self):
        print()
        print("++++++++++++++++ información de la partida +++++++++++++++++")
        print("  - Jugadores:  ")

        for jug in self.__jugadores.values():
            print("               * {0}".format(jug))

        print("  - Parámetros:  ")  
        print("                # Preguntas = {0}".format(self.__modo.num_preguntas))  
        print("                # Tiempo partida = {0} segundos".format(self.__modo.tmax_juego))
        print("                # Tiempo respuestas = {0} segundos".format(self.__modo.tmax_pregunta))  
        print("  - Marcadores:  ")  

        for jug in self.__jugadores.values():
            print("                + {0} = {1} puntos en la partida".format(jug.nombre, self.__marcadores[jug.nombre]))
        print()
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

   
        
    def finalizar(self):
        pass

    def barajar(self):
        pass

    def comprobar_respuesta(self, indice_preg, indice_resp_contestada):
        # necesitmaos el id de la pregunta y el id de la respuesta
        eso = self.preguntas[indice_preg].l_obj_respuestas[indice_resp_contestada].correcta
        return eso == 1

    def actualizar_puntos(self, nombre_jugador):
        # si comprobar_respuesta es verdad --> jugador.resultado += 1
        a = self.__marcadores
        self.__marcadores[nombre_jugador] += 1
        self.__jugadores['player_act'].resultado += 1
        self.__jugadores['player_act'].total_puntos += 1
        tmp = 1