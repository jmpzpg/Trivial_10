from settings import TEMPLATES,BD,STATIC_FILES
from bottle import run, route, jinja2_view, TEMPLATE_PATH, request, redirect, static_file
from sql import Sql

class Articulos():
    def __init__(self,id='', codigo = '', descripcion = '', precio = 0) -> None:
        self.id = id
        self.codigo = codigo
        self.descripcion = descripcion
        self.precio = precio

bdatos = Sql(BD)
TEMPLATE_PATH.append(TEMPLATES)
# art = Articulos(codigo='3x3',descripcion='Uno nuevo',precio =100)
# nuevo_id = bdatos.insert(art)
# print(f'Nuevo id = {nuevo_id}')
# registro = bdatos.select(f'select * from articulos where id ="{nuevo_id}"')
# print(f'Registro = {registro}')

# art.descripcion='Modificado XXXX'
# art.id = nuevo_id
# bdatos.update(art)
# registro = bdatos.select(f'select * from articulos where id ="{nuevo_id}"')
# print(f'Registro Modificado = {registro}')

# bdatos.delete(art)
# registro = bdatos.select(f'select * from articulos where id ="{nuevo_id}"')
# print(f'Registro Borrado = {registro}')

@route('/static/<filename:path>')
def server_static(filename):
    archivo = static_file(filename, root=STATIC_FILES)
    return archivo

@route('/')
@jinja2_view('home.html')
def lista():
    registros = bdatos.select(f'select * from articulos')
    return {'rows':registros}

@route('/ins')
@jinja2_view('formulario.html')
def nuevo():
    return {}

@route('/edit/<id:int>')
@jinja2_view('formulario.html')
def editar(id):
    fila = bdatos.select(f'select * from articulos where id ={id}')
    if fila:
        return {'row':fila[0]}
    else:
        return {}

@route('/del/<el_id:int>')
def borrar(el_id):
    art = Articulos(id=el_id)
    bdatos.delete(art)
    redirect('/')

@route('/save', method='POST')
def guardar():
    art = Articulos()
    art.id = request.POST.id.strip()
    art.codigo = request.POST.codigo.strip()
    art.descripcion = request.POST.descripcion.strip()
    art.precio = request.POST.precio.strip()
    if request.POST.id.strip(): #Actualizar
        bdatos.update(art)
    else:
        bdatos.insert(art)
    redirect('/')
    
        


run(host='localhost', port=8000,debug=True,reloader=True)