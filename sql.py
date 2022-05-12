from curses.ascii import isdigit
import sqlite3

class Sqlite():
    """
    Clase para gestionar el CRUD con la base de datos sqlite.
    - Conectarse a la base de datos
    - CREAR tabla
    - Insertar
    - Seleccionar   
    - Actualizar
    - Borrar
    """

    def __init__(self, bd) -> None:
        """
        Inicializa la clase con la propiedad nombre de la bd
        """
        self.__base_datos = bd

    @property
    def nombre(self):
        return self.__base_datos
    # -------------------------------------------------------------

    @property
    def conectar(self):
        """
        Conecta/desconecta el código con la base de datos. Devuelve el conector
        """
        try:
            cnx = sqlite3.connect(self.__base_datos)
            return cnx
        except sqlite3.OperationalError as error:
            print("Ocurrió un error: ", error)

    # -------------------------------------------------------------

    def crear_tabla(self, nombre_tabla, cadena_campos):
         
        consulta = self.__preparar_creacion(nombre_tabla, cadena_campos)
        try:
            cnx = self.conectar
            cursor = cnx.cursor()
            cursor.execute(consulta)
            return cursor.rowcount
        except sqlite3.OperationalError as error:
            print("Ocurrió un error: ", error)


    # -------------------------------------------------------------

    def leer_tabla(self, tabla, aleatorio=0, limit=0):
        """
        Ejecuta la consulta de selección de todos los campos de la tabla dada.
        Devuelve una lista con todos los registros.
        Si hace aleatorio = 1 se devolverán en orden aleatorio.
        Limit indica el número de filas a devolver. 
        """
        try:
            if aleatorio and not limit:
                consulta = "select * from {0} order by random()".format(tabla)
            elif aleatorio and limit:
                consulta = "select * from {0} order by random() limit {1}".format(tabla, limit)
            elif not aleatorio and limit:
                consulta = "select * from {0} limit {1}".format(tabla, limit)
            else:
                consulta = "select * from {0}".format(tabla)
            cnx = self.conectar
            cursor = cnx.cursor()
            cursor.execute(consulta)
            resultado = cursor.fetchall()
            return resultado
        except sqlite3.OperationalError as error:
            print("Ocurrió un error: ", error)

    # -------------------------------------------------------------

    def leer_tabla_condicion(self, tabla, campo_cond, valor_cond):
        """
        Ejecuta la consulta de selección de todos los campos de la tabla dada.
        Devuelve una lista con todos los registros que cumplan la condicion dada. 
        """
        try:
            consulta = "select * from {0} where {1} = {2}".format(tabla, campo_cond, valor_cond)
            cnx = self.conectar
            cursor = cnx.cursor()
            cursor.execute(consulta)
            resultado = cursor.fetchall()
            return resultado
        except sqlite3.OperationalError as error:
            print("Ocurrió un error: ", error)

    # -------------------------------------------------------------


    def borrar_registro(self, tabla, campo_id, valor_id): # Para no dar por supuesto que tenga un campo id
        """
        Ejecuta la consulta de borrado del registro dado, de la tabla dada.
        Hace el commit y cierra la conexión
        """
        try:
            consulta = f"delete from {tabla} where {campo_id} = {valor_id}"
            cnx = self.conectar
            cursor = cnx.cursor()
            cursor.execute(consulta)
            cnx.commit()
            cnx.close()
        except sqlite3.OperationalError as error:
            print("Ocurrió un error: ", error)

    # -------------------------------------------------------------

    def insertar_registro(self, tabla, cadena_campos, cadena_valores):
        """
            Añade un nuevos registro (dado) a la tabla pasada como parámetro.
            La listas de campos y de valores deben tener el mismo número de elemntos.
            Devuelve el índice del nuevo registro
        """
        if self.__validar_entrada(cadena_campos, cadena_valores):
            try:
                cnx = self.conectar
                consulta = self.__preparar_consulta_ins(tabla, cadena_campos, cadena_valores)
                cursor = cnx.cursor()
                cursor.execute(consulta)
                cnx.commit()
                salida = cursor.lastrowid       # id del nuevo registro
                cnx.close()
                return salida
            except sqlite3.OperationalError as error:
                print("Ocurrió un error: ", error)
        else:
            print('Las listas de campos y de valores deben de tener el mismo número de elementos')

    # -------------------------------------------------------------

    def actualizar_registro(self, tabla, cadena_campos, cadena_valores, campo_id, valor_id):
        """
            Modifica un registro (dado) en la tabla pasada como parámetro.
            La listas de campos y de valores deben tener el mismo número de elemntos.
            Devuelve la cuenta de registros actualizados/modificados. Normalmente será 1 y cierra la conexión.
        """
        if self.__validar_entrada(cadena_campos, cadena_valores):
            try:
                cnx = self.conectar
                cursor = cnx.cursor()
                consulta = self.__preparar_consulta_act(self, tabla, cadena_campos, cadena_valores, campo_id, valor_id)
                cursor.execute(consulta)
                cnx.commit()
                salida = cursor.rowcount        # número de registros modificados. Normalmente 1
                cnx.close()
                return salida
            except sqlite3.OperationalError as error:
                print("Ocurrió un error: ", error)
        else:
            print('Las listas de campos y de valores deben de tener el mismo número de elementos')

    # -------------------------------------------------------------

    def actualizar_registro_solo_puntos(self, tabla, cadena_campos, cadena_valores, campo_id, valor_id):
        """
            Modifica un registro (dado) en la tabla pasada como parámetro.
            La listas de campos y de valores solo tienen un elemento.
            Devuelve la cuenta de registros actualizados/modificados. Normalmente será 1 y cierra la conexión.
        """
        
        try:
            cnx = self.conectar
            cursor = cnx.cursor()
            consulta = self.__preparar_consulta_act_solo_puntos(tabla, cadena_campos, cadena_valores, campo_id, valor_id)
            cursor.execute(consulta)
            cnx.commit()
            salida = cursor.rowcount        # número de registros modificados. Normalmente 1
            cnx.close()
            return salida
        except sqlite3.OperationalError as error:
            print("Ocurrió un error: ", error)
        

    # -------------------------------------------------------------

    

    # -------------------------------------------------------------


    def __validar_entrada(self, in1, in2):
        return len(self.__cadena_a_lista(in1)) == len(self.__cadena_a_lista(in2))

    # -------------------------------------------------------------

    def __preparar_consulta_act_solo_puntos(self, tabla, cadena_campos, cadena_valores, campo_id, valor_id):
        cadena_campo_valor = f"update {tabla} set {cadena_campos} = {cadena_valores} where {campo_id}={valor_id}"
        return cadena_campo_valor

    # -------------------------------------------------------------   

    def __preparar_consulta_act(self, tabla, cadena_campos, cadena_valores, campo_id, valor_id):
        lista_campos = self.__cadena_a_lista(cadena_campos)
        lista_valores = self.__cadena_a_lista(cadena_valores)
        cadena = f'update {tabla} set '
        for i in range(len(lista_campos)):
            if not lista_valores[i].isdigit():
                cadena += f'{lista_campos[i]} = "{lista_valores[i]}",'
            else:
                cadena += f'{lista_campos[i]} = {lista_valores[i]},'

        return f'{cadena[:-1]} where {campo_id} = {valor_id}'
    

    # -------------------------------------------------------------   
    
    def __preparar_consulta_ins(self, tabla, cadena_campos, cadena_valores):
        lista_valores = self.__cadena_a_lista(cadena_valores)
        cadena = f'insert into {tabla}({cadena_campos}) values('
        for campo in lista_valores:
            if not campo.isdigit():
                cadena += f'"{campo}",'
            else:
                cadena += f'{campo},'

        return f'{cadena[:-1]})'

    # -------------------------------------------------------------      

    def __preparar_creacion(self, nombre_tabla, cadena_campos):
        cadena = f"create table if not exists {nombre_tabla} ({cadena_campos});"
        return cadena

    # -------------------------------------------------------------        

    def __cadena_a_lista(self, cadena):
        return cadena.split(',')
        