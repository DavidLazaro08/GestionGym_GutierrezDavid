"""
Clase Cliente.
Modelo básico para representar a los clientes del gimnasio.
Gestiona sus datos principales y ofrece utilidades auxiliares.
"""

class Cliente:

    # ---------------------------------------------------------
    #   CONSTRUCTOR
    # ---------------------------------------------------------
    def __init__(
        self,
        id_cliente=None,
        nombre="",
        apellidos="",
        dni="",
        email="",
        telefono="",
        fecha_alta=None,
        estado="activo"
    ):
        # Normalización básica
        self.id_cliente = int(id_cliente) if id_cliente is not None else None

        self.nombre = nombre or ""
        self.apellidos = apellidos or ""
        self.dni = dni or ""
        self.email = email or ""
        self.telefono = telefono or ""

        # Puede venir como None desde SQLite
        self.fecha_alta = fecha_alta or ""

        # Por defecto "activo"
        self.estado = estado or "activo"

    # ---------------------------------------------------------
    #   REPRESENTACIÓN DE TEXTO
    # ---------------------------------------------------------
    def __str__(self):
        return f"{self.nombre} {self.apellidos} - DNI: {self.dni}"

    def __repr__(self):
        """Ayuda a depurar en consola."""
        return f"<Cliente {self.id_cliente}: {self.nombre_completo}>"

    # ---------------------------------------------------------
    #   CONVERSIÓN A DICCIONARIO
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

    # ---------------------------------------------------------
    #   CREACIÓN DESDE DICCIONARIO
    # ---------------------------------------------------------
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
    #   PROPIEDADES
    # ---------------------------------------------------------
    @property
    def nombre_completo(self):
        """Devuelve 'Nombre Apellidos' bien formateado."""
        nombre = self.nombre.strip()
        apellidos = self.apellidos.strip()
        return f"{nombre} {apellidos}".strip()

    @nombre_completo.setter
    def nombre_completo(self, valor):
        """
        Permite asignar 'Nombre Apellidos' directamente.
        Soporta nombres o apellidos compuestos.
        """
        partes = valor.strip().split(" ")
        if len(partes) == 1:
            self.nombre = partes[0]
            self.apellidos = ""
        else:
            self.nombre = partes[0]
            self.apellidos = " ".join(partes[1:])
