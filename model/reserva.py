"""
Clase Reserva.
Modelo para gestionar las reservas de los aparatos del gimnasio.
Incluye la fecha, el horario y la relación con cliente y aparato.
"""

class Reserva:

    # ---------------------------------------------------------
    #   CONSTRUCTOR
    #   Crea una reserva con los datos necesarios.
    # ---------------------------------------------------------
    def __init__(self, id_reserva=None, id_cliente=None, id_aparato=None,
                 fecha_reserva=None, hora_inicio=None, hora_fin=None,
                 estado="pendiente"):

        self.id_reserva = id_reserva
        self.id_cliente = id_cliente
        self.id_aparato = id_aparato
        self.fecha_reserva = fecha_reserva
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.estado = estado

    # ---------------------------------------------------------
    #   MÉTODOS ESPECIALES
    #   Representación sencilla de la reserva.
    # ---------------------------------------------------------
    def __str__(self):
        return f"Reserva #{self.id_reserva} - {self.fecha_reserva} {self.hora_inicio}-{self.hora_fin}"

    # ---------------------------------------------------------
    #   MÉTODOS DE UTILIDAD
    #   Conversión a dict y creación desde dict.
    # ---------------------------------------------------------
    def to_dict(self):
        return {
            "id_reserva": self.id_reserva,
            "id_cliente": self.id_cliente,
            "id_aparato": self.id_aparato,
            "fecha_reserva": self.fecha_reserva,
            "hora_inicio": self.hora_inicio,
            "hora_fin": self.hora_fin,
            "estado": self.estado
        }

    @staticmethod
    def from_dict(data):
        return Reserva(
            id_reserva=data.get("id_reserva"),
            id_cliente=data.get("id_cliente"),
            id_aparato=data.get("id_aparato"),
            fecha_reserva=data.get("fecha_reserva"),
            hora_inicio=data.get("hora_inicio"),
            hora_fin=data.get("hora_fin"),
            estado=data.get("estado", "pendiente")
        )
