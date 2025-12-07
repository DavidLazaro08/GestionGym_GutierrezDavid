"""
Clase Aparato.
Modelo para representar los aparatos disponibles en el gimnasio.
Incluye datos básicos como nombre, tipo y estado.
"""

class Aparato:

    # ---------------------------------------------------------
    #   CONSTRUCTOR
    #   Crea un aparato con su información principal.
    # ---------------------------------------------------------
    def __init__(self, id_aparato=None, nombre="", tipo="",
                 estado="disponible", descripcion=""):

        self.id_aparato = id_aparato
        self.nombre = nombre
        self.tipo = tipo
        self.estado = estado
        self.descripcion = descripcion

    # ---------------------------------------------------------
    #   MÉTODOS ESPECIALES
    #   Representación sencilla del aparato.
    # ---------------------------------------------------------
    def __str__(self):
        return f"{self.nombre} ({self.tipo}) - Estado: {self.estado}"

    # ---------------------------------------------------------
    #   MÉTODOS DE UTILIDAD
    #   Conversión a dict y creación desde dict.
    # ---------------------------------------------------------
    def to_dict(self):
        return {
            "id_aparato": self.id_aparato,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "estado": self.estado,
            "descripcion": self.descripcion
        }

    @staticmethod
    def from_dict(data):
        return Aparato(
            id_aparato=data.get("id_aparato"),
            nombre=data.get("nombre", ""),
            tipo=data.get("tipo", ""),
            estado=data.get("estado", "disponible"),
            descripcion=data.get("descripcion", "")
        )
