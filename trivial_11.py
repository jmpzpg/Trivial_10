from sql import Sqlite
from partida import Partida
from jugador import Jugador
from pregunta import Pregunta
from respuesta import Respuesta
from modo import Modo
import os
from bottle import (static_file,
                    route,
                    run, 
                    jinja2_view,
                    request,
                    redirect, 
                    TEMPLATE_PATH)
from settings import STATIC_FILES,BD,TEMPLATES
TEMPLATE_PATH.append(TEMPLATES)



@route('/static/<filename:path>')
def server_static(filename):
    archivo = static_file(filename, root=STATIC_FILES)
    return archivo


# =====================================================================================

modo = Modo()
lista_aleat_obj_preguntas_con_resp = []

# -------------------------------------------------------------------------------------

def actulizar_puntos_bd():        # (partida_actual)
    bd = Sqlite('trivial_sqlite.db')
    for obj_jug in partida_actual.jugadores.values():
        id_tabla = obj_jug.id
        puntos = obj_jug.total_puntos
        bd.actualizar_registro_solo_puntos('Jugador', 'total_puntos', puntos, 'id', id_tabla)


def tomar_preguntas_aleat_con_sus_resp_de_la_bd(): # (modo)
    '''
        Toma de la BD el numero de preguntas configurado en Modo. 
        Busca las respuests de cada una de esas preguntas.
        Crea los objetos pregunta y respuesta correspondiente.
        Devuelve una lista de objetos pregunta, incluyendo sus obj resp en otra lista
    '''
    if lista_aleat_obj_preguntas_con_resp:
        lista_aleat_obj_preguntas_con_resp.clear()
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


def tomar_jugadores_de_la_bd():
    bd = Sqlite('trivial_sqlite.db')
    lista_jugadores = bd.leer_tabla('Jugador')  # jugadores que hay almacenados en la BD
    dic_players = {}
    for jug in lista_jugadores:     # llenamos dic con obj jugadores from la BD. Todos los existentes
                                    # se crea 1 obj jugador para cada jugador de la BD
        dic_players[jug[1]]= Jugador(jug[1],   # campo nombre de la tabla Jugador
                                    jug[2],    # campo resultado de la tabla Jugador
                                    jug[3],    # campo total_puntos de la tabla Jugador
                                    jug[0])    # campo id de la tabla Jugador 
    return dic_players      # dic { nombre_jug : obj_jug , . . .}



# -------------------------------------------------------------------------------------

dic_jug = {'player_act': Jugador('player_act')}
lista_obj_preg_resp = tomar_preguntas_aleat_con_sus_resp_de_la_bd()
partida_actual = Partida(dic_jug, modo, lista_obj_preg_resp)          

# -------------------------------------------------------------------------------------            
# -------------------------------------------------------------------------------------

@route('/')
@jinja2_view('usuarios.html')
def home():
    dic_jug_en_bd = tomar_jugadores_de_la_bd()
    return {'jug_disponibles' : dic_jug_en_bd}

       
# -------------------------------------------------------------------------------------

@route('/jugar/<jugador>')
@jinja2_view('home.html')
def juego(jugador):
    '''
        Hemos seleccionado al jugador en la primera pantalla y ahora nos vamos a jugar la partida.
        Queremos guardar ese jugador que ha sido seleccionado para jugar la partida y terminar así de
        tener el objeto Partida completo.
    '''
    bd = Sqlite('trivial_sqlite.db')
    l_tupla_jug = bd.leer_tabla_condicion('Jugador','nombre',jugador)
    t_id = l_tupla_jug[0][0]
    t_nombre = l_tupla_jug[0][1]
    t_resultado = l_tupla_jug[0][2]
    t_total_puntos = l_tupla_jug[0][3]

    dic_jug['player_act'] = Jugador(t_nombre, t_resultado, t_total_puntos, t_id)
   
    partida_actual.jugadores = dic_jug
    partida_actual.preguntas = tomar_preguntas_aleat_con_sus_resp_de_la_bd()
    
    datos = {
        'nombre_jug': jugador,
        'preg_aleat_con_resp': partida_actual.preguntas
    }
    return datos

# -------------------------------------------------------------------------------------

@route('/correccion', method='POST')
@jinja2_view('correccion.html')
def correccion():
    aciertos = 0
    jugador_actual = dic_jug['player_act'].nombre
    dic_idpreg_idresp_seleccionada = request.POST
    i = 0
    for id_preg , id_resp_selecc in dic_idpreg_idresp_seleccionada.items():
        id_p = int(id_preg)
        id_r = int(id_resp_selecc)       
        
        for resp in lista_aleat_obj_preguntas_con_resp[i].l_obj_respuestas:
            if resp.correcta == 1 and resp.id == id_r:
                aciertos += 1 
                partida_actual.actualizar_puntos(jugador_actual)
                break
        i += 1

    actulizar_puntos_bd()
    datos = {
        'aciertos' : aciertos,
        'jugador_actual': jugador_actual
    }
    return datos


# =====================================================================================

run(host='localhost', port=8008,debug=True,reloader=True)