"""
Controlador de Reservas
Gestiona la lógica de negocio relacionada con las reservas del gimnasio.
"""

from data.gestor_bd import GestorBD
from model.reserva import Reserva
from util.validaciones import (
    validar_fecha,
    validar_hora,
    validar_dia_laboral,
    validar_duracion_30min
)

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
    #   VALIDACIÓN CENTRALIZADA
    # ---------------------------------------------------------
    def validar_reserva(self, id_cliente, id_aparato, fecha, hora_inicio, hora_fin):
        """
        Centraliza todas las validaciones de la reserva.
        Devuelve: (True, None) si todo ok
                  (False, "mensaje de error") si algo falla
        """

        # Fecha válida
        if not validar_fecha(fecha):
            return False, "La fecha debe tener formato YYYY-MM-DD."

        # Solo lunes a viernes
        if not validar_dia_laboral(fecha):
            return False, "Las reservas solo pueden hacerse de lunes a viernes."

        # Horas válidas
        if not validar_hora(hora_inicio):
            return False, "Hora de inicio inválida."

        if not validar_hora(hora_fin):
            return False, "Hora de fin inválida."

        # Duración 30 minutos EXACTOS
        if not validar_duracion_30min(hora_inicio, hora_fin):
            return False, "La reserva debe durar exactamente 30 minutos."

        return True, None

    # ---------------------------------------------------------
    #   CREAR RESERVA
    # ---------------------------------------------------------
    def crear_reserva(self, id_cliente, id_aparato, fecha_reserva,
                      hora_inicio, hora_fin, estado="pendiente"):
        """
        Intenta crear una reserva si el aparato está libre en ese horario.
        Devuelve el ID de la reserva o None si no se puede.
        """

        # Comprobación rápida de orden
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
    #   OBTENER TODAS LAS RESERVAS (MODELO PURO)
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
    #   OBTENER RESERVAS CON NOMBRES (PARA LA VISTA)
    # ---------------------------------------------------------
    def obtener_reservas_con_nombres(self):
        """
        Devuelve una lista de diccionarios:
        [
           {
             "id_reserva": ...,
             "cliente": "Nombre Apellido",
             "aparato": "Cinta de correr",
             "fecha": ...,
             "inicio": ...,
             "fin": ...,
             "estado": ...
           }
        ]
        """
        try:
            self.db.conectar()
            query = """
                SELECT r.id_reserva,
                       c.nombre || ' ' || c.apellidos AS cliente,
                       a.nombre AS aparato,
                       r.fecha_reserva,
                       r.hora_inicio,
                       r.hora_fin,
                       r.estado
                FROM Reserva r
                JOIN Cliente c ON r.id_cliente = c.id_cliente
                JOIN Aparato a ON r.id_aparato = a.id_aparato
                ORDER BY r.id_reserva DESC
            """
            filas = self.db.obtener_datos(query)
            self.db.desconectar()
        except Exception as e:
            raise DBConsultaError("Error al obtener las reservas con nombres") from e

        lista = []
        for f in filas:
            lista.append({
                "id_reserva": f[0],
                "cliente": f[1],
                "aparato": f[2],
                "fecha": f[3],
                "inicio": f[4],
                "fin": f[5],
                "estado": f[6]
            })
        return lista

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
    #   RESERVAS FILTRADAS
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

    # ---------------------------------------------------------
    #   INFORME DE DISPONIBILIDAD
    # ---------------------------------------------------------
    def generar_informe_disponibilidad(self, fecha):
        try:
            self.db.conectar()

            query_aparatos = "SELECT id_aparato, nombre FROM Aparato ORDER BY id_aparato"
            aparatos = self.db.obtener_datos(query_aparatos)

            informe = {}

            for id_aparato, nombre_aparato in aparatos:
                query_res = """
                    SELECT r.hora_inicio, r.hora_fin, c.nombre, c.apellidos
                    FROM Reserva r
                    JOIN Cliente c ON r.id_cliente = c.id_cliente
                    WHERE r.id_aparato = ?
                    AND r.fecha_reserva = ?
                    AND r.estado != 'cancelada'
                    ORDER BY r.hora_inicio
                """

                filas = self.db.obtener_datos(query_res, (id_aparato, fecha))

                lista = []
                for h1, h2, nom, ape in filas:
                    lista.append((h1, h2, f"{nom} {ape}"))

                informe[id_aparato] = {
                    "nombre": nombre_aparato,
                    "reservas": lista
                }

            self.db.desconectar()
            return informe

        except Exception as e:
            raise DBConsultaError(f"Error al generar informe de disponibilidad: {e}") from e
