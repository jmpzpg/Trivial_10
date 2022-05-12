import os
from bottle import route, run,TEMPLATE_PATH,jinja2_view,static_file, request, redirect
import sqlite3

TEMPLATE_PATH.append(os.path.join(os.path.dirname(__file__), 'templates/'))
BASE_DATOS = os.path.join(os.path.dirname(__file__),'trivial_sqlite.db' )



@route('/static/<filename:path>')
def server_static(filename):
    return static_file(filename,root='./static')

@route('/')
@jinja2_view('home2.html')
def hola():
    cnx = sqlite3.connect(BASE_DATOS)
    consulta = """SELECT p.id, p.nombre,p.apelllidos ,p.dni ,to2.descripcion,tn.descripcion 
                from persona p left join T_ocupacion to2 
                on p.id_ocupacion =to2.id left join T_numero tn on tn.id=p.id_numero """
    cursor = cnx.execute(consulta)
    filas = cursor.fetchall()
    cnx.close()
    return {"datos": filas}

@route('/editar')
@route('/editar/<id:int>')
@jinja2_view('formulario2.html')
def mi_form(id=None):
    # Ocupaciones
    cnx = sqlite3.connect(BASE_DATOS)
    consulta = "select * from T_ocupacion"
    cursor = cnx.execute(consulta)
    ocupaciones = cursor.fetchall()

    #Números
    consulta = "select * from T_numero"
    cursor = cnx.execute(consulta)
    numeros = cursor.fetchall()

    #Vehículos
    consulta = "select * from T_vehiculo"
    cursor = cnx.execute(consulta)
    vehiculos = cursor.fetchall()


    if id is None: #Estamos en un alta
        return {'ocupaciones':ocupaciones, 'numeros':numeros,'vehiculos':vehiculos}
    else:
        consulta = "select id,nombre, apelllidos,dni, id_ocupacion, id_numero from persona where id =?"
        cursor = cnx.execute(consulta,(id,))
        filas = cursor.fetchone()

        # Mis vehículos
        consulta = f"select id_vehiculo from persona_vh where id_persona = {id}"
        cursor = cnx.execute(consulta)
        tmp = cursor.fetchall()
        mis_vehiculos = []
        for t in tmp:
            mis_vehiculos.append(t[0])

    cnx.close()
    return {'datos': filas,
            'ocupaciones':ocupaciones, 
            'numeros':numeros,
            'vehiculos':vehiculos,
            'mis_vehiculos': mis_vehiculos}

@route('/guardar', method='POST')
def guardar():
    nombre = request.POST.nombre
    apellidos = request.POST.apellidos
    dni = request.POST.dni
    id = request.POST.id
    ocupacion = request.POST.ocupacion
    numero = request.POST.numero

    #Lista de vehículos
    vehiculos = request.POST.dict['vehiculo']
    
    cnx = sqlite3.connect(BASE_DATOS)
    
    if id =='': #Alta
        consulta = "insert into persona(nombre, apelllidos,dni, id_ocupacion, id_numero) values (?,?,?,?,?)"
        tmp = cnx.execute(consulta,(nombre,apellidos,dni,ocupacion, numero))
        nuevo_id = tmp.lastrowid
        # --------------
        for v in vehiculos:
            nuevos_vh = f"""insert into persona_vh(id_persona,id_vehiculo) 
            values({nuevo_id},{v})"""
            cnx.execute(nuevos_vh)
        

    else: #Actualización
        consulta = "update persona set nombre = ?, apelllidos = ?, dni =?, id_ocupacion=?, id_numero=? where id =?"
        cnx.execute(consulta,(nombre,apellidos,dni,ocupacion,numero,id))

        # Mis vehículos
        #Borro todos los vehículos de una persona e inserto los nuevos
        consulta = f'delete from persona_vh where id_persona= {id}'
        cnx.execute(consulta)
        # --------------
        for v in vehiculos:
            nuevos_vh = f"""insert into persona_vh(id_persona,id_vehiculo) 
            values({id},{v})"""
            cnx.execute(nuevos_vh)

    cnx.commit()
    cnx.close()
    redirect('/')

@route('/borrar/<id:int>')
def borrar(id):
    cnx = sqlite3.connect(BASE_DATOS)
    consulta = f'delete from persona where id="{id}"'
    cnx.execute(consulta) 
    cnx.commit()
    cnx.close()
    redirect('/')


print(TEMPLATE_PATH)
print(BASE_DATOS)
run(host= 'localhost',port=8000, debug=True)