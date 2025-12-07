"""
Clase Cliente.
Modelo básico para representar a los clientes del gimnasio.
Guarda sus datos principales y ofrece algunos métodos de apoyo.
"""

class Cliente:

    # ---------------------------------------------------------
    #   CONSTRUCTOR
    #   Crea un nuevo cliente con sus datos esenciales.
    # ---------------------------------------------------------
    def __init__(self, id_cliente=None, nombre="", apellidos="", dni="",
                 email="", telefono="", fecha_alta=None, estado="activo"):

        self.id_cliente = id_cliente
        self.nombre = nombre
        self.apellidos = apellidos
        self.dni = dni
        self.email = email
        self.telefono = telefono
        self.fecha_alta = fecha_alta
        self.estado = estado

    # ---------------------------------------------------------
    #   MÉTODOS ESPECIALES
    #   Representación sencilla del cliente al imprimirlo.
    # ---------------------------------------------------------
    def __str__(self):
        return f"{self.nombre} {self.apellidos} - DNI: {self.dni}"

    # ---------------------------------------------------------
    #   MÉTODOS DE UTILIDAD
    #   Conversión a dict y creación desde dict.
    # ---------------------------------------------------------
    def to_dict(self):
        return {
            "id_cliente": self.id_cliente,
            "nombre": self.nombre,
            "apellidos": self.apellidos,
            "dni": self.dni,
            "email": self.email,
            "telefono": self.telefono,
            "fecha_alta": self.fecha_alta,
            "estado": self.estado
        }

    @staticmethod
    def from_dict(data):
        return Cliente(
            id_cliente=data.get("id_cliente"),
            nombre=data.get("nombre", ""),
            apellidos=data.get("apellidos", ""),
            dni=data.get("dni", ""),
            email=data.get("email", ""),
            telefono=data.get("telefono", ""),
            fecha_alta=data.get("fecha_alta"),
            estado=data.get("estado", "activo")
        )

    # ---------------------------------------------------------
    #   PROPIEDADES OPCIONALES
    #   Acceso cómodo al nombre completo.
    # ---------------------------------------------------------
    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellidos}"

    @nombre_completo.setter
    def nombre_completo(self, valor):
        partes = valor.split(" ", 1)
        self.nombre = partes[0]
        self.apellidos = partes[1] if len(partes) > 1 else ""
