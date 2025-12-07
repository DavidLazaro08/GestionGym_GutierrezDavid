"""
Controlador de Reservas
Gestiona la lógica de negocio relacionada con las reservas del gimnasio.
"""

from data.gestor_bd import GestorBD
from model.reserva import Reserva
from excepciones import (
    DBConexionError,
    DBConsultaError,
    DBInsercionError,
    DBActualizacionError,
    DBEliminacionError
)

class ReservaController:
    """Controlador responsable de operar sobre las reservas."""

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
        Intenta crear una reserva si el aparato está libre en ese horario.
        Devuelve el ID de la reserva o None si no se puede.
        """

        # Comprobación interna básica
        if hora_inicio >= hora_fin:
            return None

        # Comprobar disponibilidad real
        if not self.verificar_disponibilidad(id_aparato, fecha_reserva, hora_inicio, hora_fin):
            return None

        try:
            self.db.conectar()
        except Exception as e:
            raise DBConexionError("No se pudo conectar para crear la reserva") from e

        datos = {
            "id_cliente": id_cliente,
            "id_aparato": id_aparato,
            "fecha_reserva": fecha_reserva,
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin,
            "estado": estado
        }

        try:
            nuevo_id = self.db.insertar("Reserva", datos)
            self.db.desconectar()
            return nuevo_id
        except Exception as e:
            self.db.desconectar()
            raise DBInsercionError("Ocurrió un error al insertar la reserva") from e

    # ---------------------------------------------------------
    #   OBTENER RESERVA POR ID
    # ---------------------------------------------------------
    def obtener_reserva(self, id_reserva):
        try:
            self.db.conectar()
            query = "SELECT * FROM Reserva WHERE id_reserva = ?"
            resultado = self.db.obtener_datos(query, (id_reserva,))
            self.db.desconectar()
        except Exception as e:
            raise DBConsultaError("Error al consultar la reserva por ID") from e

        if not resultado:
            return None

        f = resultado[0]
        return Reserva(*f)

    # ---------------------------------------------------------
    #   OBTENER TODAS LAS RESERVAS
    # ---------------------------------------------------------
    def obtener_todas_reservas(self):
        try:
            self.db.conectar()
            filas = self.db.obtener_datos("SELECT * FROM Reserva")
            self.db.desconectar()
        except Exception as e:
            raise DBConsultaError("Error al obtener todas las reservas") from e

        return [Reserva(*f) for f in filas]

    # ---------------------------------------------------------
    #   ACTUALIZAR RESERVA
    # ---------------------------------------------------------
    def actualizar_reserva(self, id_reserva, **kwargs):
        try:
            self.db.conectar()
            ok = self.db.actualizar("Reserva", kwargs, f"id_reserva = {id_reserva}")
            self.db.desconectar()
            return ok
        except Exception as e:
            raise DBActualizacionError("Error al actualizar la reserva") from e

    # ---------------------------------------------------------
    #   ELIMINAR RESERVA
    # ---------------------------------------------------------
    def eliminar_reserva(self, id_reserva):
        try:
            self.db.conectar()
            ok = self.db.eliminar("Reserva", f"id_reserva = {id_reserva}")
            self.db.desconectar()
            return ok
        except Exception as e:
            raise DBEliminacionError("Error al eliminar la reserva") from e

    # ---------------------------------------------------------
    #   RESERVAS POR CLIENTE / APARATO / FECHA
    # ---------------------------------------------------------
    def obtener_reservas_por_cliente(self, id_cliente):
        try:
            self.db.conectar()
            filas = self.db.obtener_datos(
                "SELECT * FROM Reserva WHERE id_cliente = ?",
                (id_cliente,)
            )
            self.db.desconectar()
            return [Reserva(*f) for f in filas]
        except Exception as e:
            raise DBConsultaError("Error al obtener reservas del cliente") from e

    def obtener_reservas_por_aparato(self, id_aparato):
        try:
            self.db.conectar()
            filas = self.db.obtener_datos(
                "SELECT * FROM Reserva WHERE id_aparato = ?",
                (id_aparato,)
            )
            self.db.desconectar()
            return [Reserva(*f) for f in filas]
        except Exception as e:
            raise DBConsultaError("Error al obtener reservas del aparato") from e

    def obtener_reservas_por_fecha(self, fecha):
        try:
            self.db.conectar()
            filas = self.db.obtener_datos(
                "SELECT * FROM Reserva WHERE fecha_reserva = ?",
                (fecha,)
            )
            self.db.desconectar()
            return [Reserva(*f) for f in filas]
        except Exception as e:
            raise DBConsultaError("Error al obtener reservas por fecha") from e

    # ---------------------------------------------------------
    #   VERIFICAR DISPONIBILIDAD
    # ---------------------------------------------------------
    def verificar_disponibilidad(self, id_aparato, fecha, hora_inicio, hora_fin):
        """
        Verifica si existe solapamiento horario con reservas previas.
        Un intervalo solapa si:
                inicio1 < fin2   Y   inicio2 < fin1
        """

        try:
            self.db.conectar()
            query = """
                SELECT COUNT(*)
                FROM Reserva
                WHERE id_aparato = ?
                AND fecha_reserva = ?
                AND estado != 'cancelada'
                AND (
                    hora_inicio < ?   -- fin nueva
                    AND ? < hora_fin  -- inicio nueva
                )
            """

            res = self.db.obtener_datos(query, (id_aparato, fecha, hora_fin, hora_inicio))
            self.db.desconectar()
            return res[0][0] == 0
        except Exception as e:
            raise DBConsultaError("Error al verificar disponibilidad del aparato") from e
