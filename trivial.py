from sql import Sqlite
from partida import Partida
from jugador import Jugador
from pregunta import Pregunta
from respuesta import Respuesta
from modo import Modo
import os



def main():
    ''' Motor del juego
    '''
    # primero hay que cargar un modo para confirmar por el usuario:
    modo = Modo()
    # Mostramos pantalla con menú del juego según los datos del modo actual:
    continuar = True
    while(continuar):
        eleccion_correcta = False
        while( not eleccion_correcta ):
            os.system('clear')
            opcion = menu_ppal(modo)

            if opcion < 1 or opcion > 6:
                os.system('clear')
                print("Elección incorrecta, pruebe de nuevo...")
                print('')
            elif opcion == 1:
                print('')
                numero = int(input('Cúantos jugadores jugarán la partida?: '))
                if numero != 1:
                    os.system('clear')
                    print('Lo sentimos, la partida multijugador será soportada en la siguiente versión')
                print('')
            elif opcion == 2:
                os.system('clear')
                print('')
                seguir = True
                while( seguir ):
                    num_preg = int(input('Por favor, indique un número de preguntas entre 5 y 15: '))
                    print('')
                    if (4 < num_preg < 16):
                        modo.num_preguntas = num_preg
                        seguir = False
            elif opcion == 3:
                os.system('clear')
                print('')
                tiempo_partida = int(input('Por favor, indique un tiempo máximo para la partida, en segundos: '))
                print('')
                modo.tmax_juego = tiempo_partida
            elif opcion == 4:
                os.system('clear')
                print('')
                tiempo_pregunta = int(input('Por favor, indique un tiempo máximo para contestar cada pregunta, en segundos: '))
                print('')
                modo.tmax_pregunta = tiempo_pregunta
            elif opcion == 6:
                continuar = False
                print("¡Esperamos que se haya divertido!")
                break
            else:
                eleccion_correcta = True
                continuar = False
                print('arrancando la partida ...')
                print('')
                iniciar_partida(modo)


# =====================================================================================


def menu_ppal(modo):
    print('')
    print("===================== MENÚ PRINCIPAL ======================")
    print(" 1.- Número de jugadores  ({0})".format(modo.num_jugadores))
    print(" 2.- Número de preguntas  ({0})".format(modo.num_preguntas))
    print(" 3.- Tiempo máximo para terminar la partida  ({0} segundos)".format(modo.tmax_juego))
    print(" 4.- Tiempo máximo por pregunta  ({0} segundos)".format(modo.tmax_pregunta))
    print(" 5.- Iniciar una partida")
    print(" 6.- Salir")
    print("===========================================================")
    print('')
    opcion = int(input("Por favor, ingrese un número: "))
    return opcion

# -------------------------------------------------------------------------------------

def iniciar_partida(modo):
    os.system('clear')
    nueva_partida = True
    while(nueva_partida):
        dic_jug = bloque_jugadores()
        lista_obj_preg_resp = tomar_preguntas_aleat_con_sus_resp_de_la_bd(modo)
        
        partida_actual = Partida(dic_jug, modo, lista_obj_preg_resp)
        partida_actual.mostrar_info_partida()
        #contador = 1
        for contador in range(len(lista_obj_preg_resp)):
            os.system('clear')
            partida_actual.mostrar_info_partida()
            print('')
            bloque_pregunta(partida_actual, contador)
            partida_actual.mostrar_info_partida()
        os.system('clear')
        actulizar_puntos_bd(partida_actual)
        print('')
        partida_actual.mostrar_info_partida()
        items = list(partida_actual.marcadores.items())
        jug = items[0][0]
        pts = items[0][1]
        print('')
        print('Partida finalizada. Número de respuestas correctas = {0}. Puntos conseguidos = {1}'.format(pts,pts))
        print('')
        otra = input('No quieres jugar otra partida?. Pulsa "n" para salir: ')
        if otra == 'n' or otra == 'N':
            nueva_partida = False
    print('')
    print('        ****  ****     GAME OVER     ****  ****')
    print('')
    print('')


# -------------------------------------------------------------------------------------


def bloque_pregunta(partida, cont):
    #p = Partida({},Modo(),[])
    for k_jug in partida.jugadores.keys():
        print('')
        print("====== PREGUNTA nº {0}/{1} para el jugador < {2} > =======".format(cont+1, partida.modo.num_preguntas, k_jug))
        print("")
        print("  * ¿{0}".format(partida.preguntas[cont].cuerpo))
        print("")
        print("  - Respuestas posibles:")
        print("")
        i = 1
        for r in partida.preguntas[cont].l_obj_respuestas:
            print("          {0}.- {1}".format(i, r.cuerpo))
            i += 1
        print("")
        print("===========================================================")
        print('')
        seguir = True
        while(seguir):
            opcion = int(input("Por favor, ingrese el número de la respuesta correcta: "))
            if not (opcion < 1 and opcion > i-1):
                if partida.comprobar_respuesta(cont, opcion-1):
                    
                    print('  ¡¡¡ ACERTASTE !!!')
                    partida.actualizar_puntos(k_jug)
                else:
                    print(' -- La próxima vez tendrás mejor suerte, pero estudia más hombre !! --')
                seguir = False   
            

# -------------------------------------------------------------------------------------

def bloque_jugadores():
    bd = Sqlite('trivial_sqlite.db')
    lista_jugadores = bd.leer_tabla('Jugador')  # jugadores que hay almacenados en la BD
    dic_jugadores_partida = {}
    dic_players = {}
          
    for jug in lista_jugadores:     # llenamos dic con obj jugadores from la BD. Todos los existentes
                                    # se crea 1 obj jugador para cada jugador de la BD
        dic_players[jug[1]]= Jugador(jug[1],   # campo nombre de la tabla Jugador
                                    jug[2],    # campo resultado de la tabla Jugador
                                    jug[3],    # campo total_puntos de la tabla Jugador
                                    jug[0])    # campo id de la tabla Jugador 
    dic_items = {}
    seguir = True
    while(seguir):
        os.system('clear')
        print('')
        print("===================== Elija jugador: ======================")
        print('')
        print("      1.- Jugador: NUEVO jugador !!! ")
        i = 2
        for obj_jugador in dic_players.values():
            print('')
            print("      {0}.- {1} ".format(i, obj_jugador))
            dic_items[i] = obj_jugador
            i += 1
        ultimo = i-1
        print('')
        print("===========================================================")
        print('')
        opcion = int(input("Por favor, ingrese un número: "))
        if opcion < 1 or opcion > ultimo:
            
            print("Elección incorrecta, prueba de nuevo...")
            print('')
        elif opcion == 1:       # crear nuevo jugador y meterlo en la base de datos
            nom = input('Por favor, introduce un nombre para el jugador: ')
            indice = bd.insertar_registro('Jugador','nombre', nom)     # indice de la nueva fila
            tmp = Jugador(nom,id_tabla=indice)                            # lo usamos al instanciar el obj.
            dic_jugadores_partida[nom] = tmp            # este nuevo jugador será el que juegue la partida
            seguir = False
        else:
            for k,v in dic_items.items():
                if opcion == k:
                    dic_jugadores_partida[v.nombre] = v # este jugador será el que juegue la partida
                    seguir = False
                    print('')
                    print('La partida se jugará con el jugador "{0}" de nombre "{1}" '.format(k,v.nombre))
    return dic_jugadores_partida
              
# -------------------------------------------------------------------------------------

def tomar_preguntas_aleat_con_sus_resp_de_la_bd(modo):
    '''
        Toma de la BD el numero de preguntas configurado en Modo. 
        Busca las respuests de cada una de esas preguntas.
        Crea los objetos pregunta y respuesta correspondiente.
        Devuelve una lista de objetos pregunta, incluyendo sus obj resp en otra lista
    '''
    lista_aleat_obj_preguntas_con_resp = []
    num_preguntas = modo.num_preguntas
    bd = Sqlite('trivial_sqlite.db')                 # filas_aleat_preg es una lista de tuplas [(id,cuerpo,tema_id,dific_id)*num_preg]
    filas_aleat_preg = bd.leer_tabla('Pregunta', 1, limit=num_preguntas)  # el 1 indica que el select sea aleatorio
    for fila in filas_aleat_preg:                            
        resp = bd.leer_tabla_condicion('Respuesta', 'pregunta_id', fila[0])     # resp es una lista con 4 tuplas respuesta
        lista_obj_respuestas_de_preg = []                                       # [(id,cuerpo,correcta,preg_id) * 4]
        for t in resp:
            tmp = Respuesta(t[0], t[1], t[2])   # obj Respuesta = id ,cuerpo, correcta
            lista_obj_respuestas_de_preg.append(tmp)
        lista_aleat_obj_preguntas_con_resp.append(Pregunta(fila[0], fila[1], fila[2], fila[3], lista_obj_respuestas_de_preg))
    return lista_aleat_obj_preguntas_con_resp   # [obj Pregunta] = id, cuerpo, tema, dific, lista obj Respuesta
       
# -------------------------------------------------------------------------------------
  
def actulizar_puntos_bd(partida_actual):
    bd = Sqlite('trivial_sqlite.db')
    for obj_jug in partida_actual.jugadores.values():
        id_tabla = obj_jug.id
        puntos = obj_jug.total_puntos
        bd.actualizar_registro_solo_puntos('Jugador', 'total_puntos', puntos, 'id', id_tabla)


# =====================================================================================

main()
#bd = Sqlite('trivial_sqlite.db')
#bd.insertar_registro('Jugador','nombre','flash gordo')
#lista_jugadores = bd.leer_tabla('Jugador')
#print('final')
#print(lista_jugadores)

#bloque_jugadores()

#tomar_preguntas_aleat_con_sus_resp_de_la_bd(Modo())

#iniciar_partida(Modo())