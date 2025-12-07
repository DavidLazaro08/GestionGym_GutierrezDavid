# ---------------------------------------------------------
#   CONTROLADOR DE PAGOS
#   Gestiona toda la lógica relacionada con pagos mensuales.
# ---------------------------------------------------------

from data.gestor_bd import GestorBD
from model.pago import Pago
from datetime import date


class PagoController:

    def __init__(self):
        """Inicializa el controlador y su gestor de BD."""
        self.db = GestorBD()

    # ---------------------------------------------------------
    #   GENERAR PAGOS MENSUALES (NUEVO)
    # ---------------------------------------------------------
    def generar_pagos_mensuales(self, mes):
        """
        Genera un pago pendiente para cada cliente activo.
        mes → string "YYYY-MM".
        Evita duplicaciones: sólo crea si NO existe un pago previo para ese cliente en ese mes.
        """
        self.db.conectar()

        consulta = "SELECT id_cliente FROM Cliente WHERE estado = 'activo'"
        clientes = self.db.obtener_datos(consulta)

        fecha_generacion = str(date.today())
        creados = 0

        for fila in clientes:
            id_cliente = fila[0]

            # -------------------------------
            # 1. Verificación anti-duplicado
            # -------------------------------
            check_query = """
                SELECT COUNT(*) 
                FROM Pago 
                WHERE id_cliente = ? AND mes = ?
            """
            existe = self.db.obtener_datos(check_query, (id_cliente, mes))[0][0]

            if existe > 0:
                # Ya hay un pago ese mes → saltar
                continue

            # -------------------------------
            # 2. Crear pago nuevo
            # -------------------------------
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

        self.db.desconectar()
        return creados

    # ---------------------------------------------------------
    #   MARCAR UN PAGO COMO PAGADO (NUEVO)
    # ---------------------------------------------------------
    def marcar_pago_como_pagado(self, id_pago, fecha_pago, metodo_pago, concepto=""):
        """
        Marca un pago como pagado.
        Registra fecha, método de pago y concepto.
        """
        self.db.conectar()

        datos = {
            "pagado": 1,
            "fecha_pago": fecha_pago,
            "metodo_pago": metodo_pago,
            "concepto": concepto
        }

        resultado = self.db.actualizar("Pago", datos, f"id_pago = {id_pago}")
        self.db.desconectar()
        return resultado

    # ---------------------------------------------------------
    #   CREAR PAGO MANUAL (versión original adaptada)
    # ---------------------------------------------------------
    def crear_pago(self, id_cliente, mes, fecha_pago, metodo_pago, concepto=""):
        """
        Crea un pago manual (no automático).
        """
        self.db.conectar()

        datos = {
            "id_cliente": id_cliente,
            "mes": mes,
            "fecha_generacion": fecha_pago,  # lo más parecido al “manual”
            "pagado": 1,
            "fecha_pago": fecha_pago,
            "cuota": 30,
            "metodo_pago": metodo_pago,
            "concepto": concepto
        }

        nuevo_id = self.db.insertar("Pago", datos)
        self.db.desconectar()
        return nuevo_id

    # ---------------------------------------------------------
    #   OBTENER PAGO POR ID
    # ---------------------------------------------------------
    def obtener_pago(self, id_pago):
        """Devuelve un pago por su ID."""
        self.db.conectar()
        query = "SELECT * FROM Pago WHERE id_pago = ?"
        datos = self.db.obtener_datos(query, (id_pago,))
        self.db.desconectar()

        if not datos:
            return None

        f = datos[0]
        return Pago(f[0], f[1], f[2], f[3], f[4], f[5], f[6], f[7], f[8])

    # ---------------------------------------------------------
    #   OBTENER TODOS LOS PAGOS
    # ---------------------------------------------------------
    def obtener_todos_pagos(self):
        """Devuelve todos los pagos registrados."""
        self.db.conectar()
        filas = self.db.obtener_datos("SELECT * FROM Pago ORDER BY id_pago DESC")
        self.db.desconectar()

        pagos = []
        for f in filas:
            pagos.append(Pago(f[0], f[1], f[2], f[3], f[4], f[5], f[6], f[7], f[8]))
        return pagos

    # ---------------------------------------------------------
    #   ACTUALIZAR PAGO
    # ---------------------------------------------------------
    def actualizar_pago(self, id_pago, **kwargs):
        """
        Actualiza cualquier campo del pago.
        kwargs puede incluir: mes, fecha_generacion, pagado, fecha_pago,
                              cuota, metodo_pago, concepto.
        """
        if not kwargs:
            return False

        self.db.conectar()
        resultado = self.db.actualizar("Pago", kwargs, f"id_pago = {id_pago}")
        self.db.desconectar()
        return resultado

    # ---------------------------------------------------------
    #   ELIMINAR PAGO
    # ---------------------------------------------------------
    def eliminar_pago(self, id_pago):
        """Elimina un pago por ID."""
        self.db.conectar()
        ok = self.db.eliminar("Pago", f"id_pago = {id_pago}")
        self.db.desconectar()
        return ok

    # ---------------------------------------------------------
    #   OBTENER PAGOS POR CLIENTE
    # ---------------------------------------------------------
    def obtener_pagos_por_cliente(self, id_cliente):
        """Devuelve todos los pagos de un cliente."""
        self.db.conectar()
        filas = self.db.obtener_datos(
            "SELECT * FROM Pago WHERE id_cliente = ? ORDER BY mes DESC",
            (id_cliente,)
        )
        self.db.desconectar()

        return [Pago(f[0], f[1], f[2], f[3], f[4], f[5], f[6], f[7], f[8]) for f in filas]

    # ---------------------------------------------------------
    #   OBTENER PAGOS POR FECHA
    # ---------------------------------------------------------
    def obtener_pagos_por_fecha(self, fecha_inicio, fecha_fin=None):
        """Filtra pagos según fecha de pago."""
        self.db.conectar()

        if fecha_fin:
            query = "SELECT * FROM Pago WHERE fecha_pago BETWEEN ? AND ?"
            filas = self.db.obtener_datos(query, (fecha_inicio, fecha_fin))
        else:
            query = "SELECT * FROM Pago WHERE fecha_pago = ?"
            filas = self.db.obtener_datos(query, (fecha_inicio,))

        self.db.desconectar()

        return [Pago(f[0], f[1], f[2], f[3], f[4], f[5], f[6], f[7], f[8]) for f in filas]

    # ---------------------------------------------------------
    #   CALCULAR TOTAL PAGOS DE UN CLIENTE
    # ---------------------------------------------------------
    def calcular_total_pagos_cliente(self, id_cliente):
        """Devuelve la suma de cuotas pagadas por un cliente."""
        self.db.conectar()
        query = "SELECT SUM(cuota) FROM Pago WHERE id_cliente = ? AND pagado = 1"
        resultado = self.db.obtener_datos(query, (id_cliente,))
        self.db.desconectar()

        return resultado[0][0] if resultado and resultado[0][0] else 0.0

    # ---------------------------------------------------------
    #   OBTENER PAGOS POR MÉTODO
    # ---------------------------------------------------------
    def obtener_pagos_por_metodo(self, metodo):
        """Devuelve pagos filtrados por método de pago."""
        self.db.conectar()
        filas = self.db.obtener_datos(
            "SELECT * FROM Pago WHERE metodo_pago = ?",
            (metodo,)
        )
        self.db.desconectar()

        return [Pago(f[0], f[1], f[2], f[3], f[4], f[5], f[6], f[7], f[8]) for f in filas]
