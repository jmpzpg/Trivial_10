class Posts():
    def __init__(self, 
                id=None, 
                fecha=None, 
                autor=None, 
                titulo=None, 
                cuerpo=None,
                categorias = None,
                etiquetas = None) -> None:
        self.id = id
        self.fecha = fecha
        self.autor = autor
        self.titulo = titulo
        self.cuerpo = cuerpo
        self.categorias = categorias
        self.etiquetas = etiquetas
        

class T_Etiquetas():
    def __init__(self, id, nombre) -> None:
        self.id = id
        self.nombre = nombre

class T_Categorias():
    def __init__(self, id, nombre) -> None:
        self.id = id
        self.nombre = nombre