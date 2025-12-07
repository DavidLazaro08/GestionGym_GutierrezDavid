"""
Controlador de Reservas
Gestiona la lógica de negocio relacionada con reservas.
"""

from data.gestor_bd import GestorBD
from model.reserva import Reserva


class ReservaController:
    """Controlador para gestionar reservas."""

    # ---------------------------------------------------------
    #   CONSTRUCTOR
    # ---------------------------------------------------------
    def __init__(self):
        self.db = GestorBD()

    # ---------------------------------------------------------
    #   CREAR RESERVA
    # ---------------------------------------------------------
    def crear_reserva(self, id_cliente, id_aparato, fecha_reserva,
                      hora_inicio, hora_fin, estado="pendiente"):
        """
        Crea una nueva reserva si el aparato está libre.
        Retorna el ID o None si no se puede reservar.
        """

        if not self.verificar_disponibilidad(id_aparato, fecha_reserva,
                                             hora_inicio, hora_fin):
            return None  # aparato ocupado

        self.db.conectar()

        datos = {
            "id_cliente": id_cliente,
            "id_aparato": id_aparato,
            "fecha_reserva": fecha_reserva,
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin,
            "estado": estado
        }

        nuevo_id = self.db.insertar("Reserva", datos)
        self.db.desconectar()
        return nuevo_id

    # ---------------------------------------------------------
    #   OBTENER RESERVA POR ID
    # ---------------------------------------------------------
    def obtener_reserva(self, id_reserva):
        self.db.conectar()
        query = "SELECT * FROM Reserva WHERE id_reserva = ?"
        resultado = self.db.obtener_datos(query, (id_reserva,))
        self.db.desconectar()

        if not resultado:
            return None

        f = resultado[0]
        return Reserva(f[0], f[1], f[2], f[3], f[4], f[5], f[6])

    # ---------------------------------------------------------
    #   OBTENER TODAS LAS RESERVAS
    # ---------------------------------------------------------
    def obtener_todas_reservas(self):
        self.db.conectar()
        filas = self.db.obtener_datos("SELECT * FROM Reserva")
        self.db.desconectar()

        return [
            Reserva(f[0], f[1], f[2], f[3], f[4], f[5], f[6])
            for f in filas
        ]

    # ---------------------------------------------------------
    #   ACTUALIZAR RESERVA
    # ---------------------------------------------------------
    def actualizar_reserva(self, id_reserva, **kwargs):
        """
        Actualiza campos de la reserva.
        kwargs puede incluir: id_cliente, id_aparato, fecha_reserva,
                              hora_inicio, hora_fin, estado
        """
        self.db.conectar()
        ok = self.db.actualizar("Reserva", kwargs, f"id_reserva = {id_reserva}")
        self.db.desconectar()
        return ok

    # ---------------------------------------------------------
    #   ELIMINAR RESERVA
    # ---------------------------------------------------------
    def eliminar_reserva(self, id_reserva):
        self.db.conectar()
        ok = self.db.eliminar("Reserva", f"id_reserva = {id_reserva}")
        self.db.desconectar()
        return ok

    # ---------------------------------------------------------
    #   RESERVAS POR CLIENTE
    # ---------------------------------------------------------
    def obtener_reservas_por_cliente(self, id_cliente):
        self.db.conectar()
        q = "SELECT * FROM Reserva WHERE id_cliente = ?"
        filas = self.db.obtener_datos(q, (id_cliente,))
        self.db.desconectar()

        return [Reserva(*f) for f in filas]

    # ---------------------------------------------------------
    #   RESERVAS POR APARATO
    # ---------------------------------------------------------
    def obtener_reservas_por_aparato(self, id_aparato):
        self.db.conectar()
        q = "SELECT * FROM Reserva WHERE id_aparato = ?"
        filas = self.db.obtener_datos(q, (id_aparato,))
        self.db.desconectar()

        return [Reserva(*f) for f in filas]

    # ---------------------------------------------------------
    #   RESERVAS POR FECHA
    # ---------------------------------------------------------
    def obtener_reservas_por_fecha(self, fecha):
        self.db.conectar()
        q = "SELECT * FROM Reserva WHERE fecha_reserva = ?"
        filas = self.db.obtener_datos(q, (fecha,))
        self.db.desconectar()

        return [Reserva(*f) for f in filas]

    # ---------------------------------------------------------
    #   VERIFICAR DISPONIBILIDAD
    # ---------------------------------------------------------
    def verificar_disponibilidad(self, id_aparato, fecha, hora_inicio, hora_fin):
        """
        Comprueba si hay conflicto horario con reservas existentes.
        Lógica corregida:
        Un intervalo coincide si se solapan las horas:

              (inicio1 < fin2) y (inicio2 < fin1)
        """

        self.db.conectar()
        query = """
            SELECT COUNT(*) FROM Reserva
            WHERE id_aparato = ?
            AND fecha_reserva = ?
            AND estado != 'cancelada'
            AND (
                hora_inicio < ? AND
                ? < hora_fin
            )
        """

        # hora_inicio < hora_fin_existente  AND hora_inicio_existente < hora_fin
        res = self.db.obtener_datos(query, (id_aparato, fecha, hora_fin, hora_inicio))
        self.db.desconectar()

        return res[0][0] == 0  # True si NO hay solapamiento
