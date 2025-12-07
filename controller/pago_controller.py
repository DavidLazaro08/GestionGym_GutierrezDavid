# ---------------------------------------------------------
#   CONTROLADOR DE PAGOS
#   Gestiona toda la lógica relacionada con pagos mensuales.
# ---------------------------------------------------------

from data.gestor_bd import GestorBD
from model.pago import Pago
from excepciones import ErrorBaseDatos
from datetime import date


class PagoController:

    def __init__(self):
        """Inicializa el controlador y su gestor de BD."""
        self.db = GestorBD()

    # ---------------------------------------------------------
    #   GENERAR PAGOS MENSUALES
    # ---------------------------------------------------------
    def generar_pagos_mensuales(self, mes):
        """
        Genera un pago pendiente para cada cliente activo.
        mes → string "YYYY-MM".
        Evita duplicados: sólo crea si NO existe un pago de ese mes.
        """
        try:
            self.db.conectar()

            clientes = self.db.obtener_datos(
                "SELECT id_cliente FROM Cliente WHERE estado = 'activo'"
            )

            fecha_generacion = str(date.today())
            creados = 0

            for fila in clientes:
                id_cliente = fila[0]

                # Verificar duplicados
                existe = self.db.obtener_datos(
                    """
                    SELECT COUNT(*) FROM Pago
                    WHERE id_cliente = ? AND mes = ?
                    """,
                    (id_cliente, mes)
                )[0][0]

                if existe > 0:
                    continue

                datos = {
                    "id_cliente": id_cliente,
                    "mes": mes,
                    "fecha_generacion": fecha_generacion,
                    "pagado": 0,
                    "fecha_pago": None,
                    "cuota": 30,
                    "metodo_pago": None,
                    "concepto": None
                }

                self.db.insertar("Pago", datos)
                creados += 1

            return creados

        except Exception as e:
            raise ErrorBaseDatos(f"Error al generar pagos mensuales: {e}")

        finally:
            self.db.desconectar()

    # ---------------------------------------------------------
    #   MARCAR COMO PAGADO
    # ---------------------------------------------------------
    def marcar_pago_como_pagado(self, id_pago, fecha_pago, metodo_pago, concepto=""):
        """
        Marca un pago como pagado y registra fecha, método y concepto.
        """
        try:
            self.db.conectar()

            datos = {
                "pagado": 1,
                "fecha_pago": fecha_pago,
                "metodo_pago": metodo_pago,
                "concepto": concepto
            }

            return self.db.actualizar("Pago", datos, f"id_pago = {id_pago}")

        except Exception as e:
            raise ErrorBaseDatos(f"Error al registrar el pago: {e}")

        finally:
            self.db.desconectar()

    # ---------------------------------------------------------
    #   CREAR PAGO MANUAL
    # ---------------------------------------------------------
    def crear_pago(self, id_cliente, mes, fecha_pago, metodo_pago, concepto=""):
        """
        Crea un pago manual (ya pagado).
        """
        try:
            self.db.conectar()

            datos = {
                "id_cliente": id_cliente,
                "mes": mes,
                "fecha_generacion": fecha_pago,
                "pagado": 1,
                "fecha_pago": fecha_pago,
                "cuota": 30,
                "metodo_pago": metodo_pago,
                "concepto": concepto
            }

            return self.db.insertar("Pago", datos)

        except Exception as e:
            raise ErrorBaseDatos(f"Error al crear el pago manual: {e}")

        finally:
            self.db.desconectar()

    # ---------------------------------------------------------
    #   OBTENER PAGO POR ID
    # ---------------------------------------------------------
    def obtener_pago(self, id_pago):
        """Devuelve un pago por su ID."""
        try:
            self.db.conectar()
            datos = self.db.obtener_datos(
                "SELECT * FROM Pago WHERE id_pago = ?",
                (id_pago,)
            )
        except Exception as e:
            raise ErrorBaseDatos(f"Error consultando el pago: {e}")
        finally:
            self.db.desconectar()

        if not datos:
            return None

        f = datos[0]
        return Pago(f[0], f[1], f[2], f[3], f[4], f[5], f[6], f[7], f[8])

    # ---------------------------------------------------------
    #   OBTENER TODOS LOS PAGOS
    # ---------------------------------------------------------
    def obtener_todos_pagos(self):
        try:
            self.db.conectar()
            filas = self.db.obtener_datos(
                "SELECT * FROM Pago ORDER BY id_pago DESC"
            )
        except Exception as e:
            raise ErrorBaseDatos(f"Error obteniendo los pagos: {e}")
        finally:
            self.db.desconectar()

        return [Pago(*f) for f in filas]

    # ---------------------------------------------------------
    #   ACTUALIZAR PAGO
    # ---------------------------------------------------------
    def actualizar_pago(self, id_pago, **kwargs):
        if not kwargs:
            return False
        try:
            self.db.conectar()
            return self.db.actualizar("Pago", kwargs, f"id_pago = {id_pago}")
        except Exception as e:
            raise ErrorBaseDatos(f"Error actualizando pago: {e}")
        finally:
            self.db.desconectar()

    # ---------------------------------------------------------
    #   ELIMINAR PAGO
    # ---------------------------------------------------------
    def eliminar_pago(self, id_pago):
        try:
            self.db.conectar()
            return self.db.eliminar("Pago", f"id_pago = {id_pago}")
        except Exception as e:
            raise ErrorBaseDatos(f"Error eliminando pago: {e}")
        finally:
            self.db.desconectar()

    # ---------------------------------------------------------
    #   PAGOS POR CLIENTE
    # ---------------------------------------------------------
    def obtener_pagos_por_cliente(self, id_cliente):
        try:
            self.db.conectar()
            filas = self.db.obtener_datos(
                "SELECT * FROM Pago WHERE id_cliente = ? ORDER BY mes DESC",
                (id_cliente,)
            )
        except Exception as e:
            raise ErrorBaseDatos(f"Error consultando pagos del cliente: {e}")
        finally:
            self.db.desconectar()

        return [Pago(*f) for f in filas]

    # ---------------------------------------------------------
    #   PAGOS POR FECHA
    # ---------------------------------------------------------
    def obtener_pagos_por_fecha(self, fecha_inicio, fecha_fin=None):
        try:
            self.db.conectar()

            if fecha_fin:
                query = "SELECT * FROM Pago WHERE fecha_pago BETWEEN ? AND ?"
                filas = self.db.obtener_datos(query, (fecha_inicio, fecha_fin))
            else:
                query = "SELECT * FROM Pago WHERE fecha_pago = ?"
                filas = self.db.obtener_datos(query, (fecha_inicio,))

        except Exception as e:
            raise ErrorBaseDatos(f"Error filtrando pagos por fecha: {e}")

        finally:
            self.db.desconectar()

        return [Pago(*f) for f in filas]

    # ---------------------------------------------------------
    #   TOTAL PAGADO POR CLIENTE
    # ---------------------------------------------------------
    def calcular_total_pagos_cliente(self, id_cliente):
        try:
            self.db.conectar()
            resultado = self.db.obtener_datos(
                "SELECT SUM(cuota) FROM Pago WHERE id_cliente = ? AND pagado = 1",
                (id_cliente,)
            )
        except Exception as e:
            raise ErrorBaseDatos(f"Error calculando total pagado: {e}")
        finally:
            self.db.desconectar()

        return resultado[0][0] if resultado and resultado[0][0] else 0.0

    # ---------------------------------------------------------
    #   PAGOS POR MÉTODO
    # ---------------------------------------------------------
    def obtener_pagos_por_metodo(self, metodo):
        try:
            self.db.conectar()
            filas = self.db.obtener_datos(
                "SELECT * FROM Pago WHERE metodo_pago = ?",
                (metodo,)
            )
        except Exception as e:
            raise ErrorBaseDatos(f"Error filtrando por método: {e}")
        finally:
            self.db.desconectar()

        return [Pago(*f) for f in filas]
