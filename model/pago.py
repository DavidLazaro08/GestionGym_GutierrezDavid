"""
Clase Pago.
Modelo para gestionar los pagos mensuales de los clientes.
Incluye el mes del recibo, su estado y datos complementarios.
"""

class Pago:

    # ---------------------------------------------------------
    #   CONSTRUCTOR
    # ---------------------------------------------------------
    def __init__(
        self,
        id_pago=None,
        id_cliente=None,
        mes="",
        fecha_generacion=None,
        pagado=False,
        fecha_pago=None,
        cuota=0.0,
        metodo_pago="",
        concepto=""
    ):
        self.id_pago = id_pago
        self.id_cliente = id_cliente
        self.mes = mes
        self.fecha_generacion = fecha_generacion

        # SQLite devuelve 0/1 → convertimos a bool
        self.pagado = bool(pagado)

        self.fecha_pago = fecha_pago

        # Asegurar tipo float
        self.cuota = float(cuota) if cuota is not None else 0.0

        # Evitar problemas si vienen como None
        self.metodo_pago = metodo_pago or ""
        self.concepto = concepto or ""

    # ---------------------------------------------------------
    #   REPRESENTACIÓN DE TEXTO
    # ---------------------------------------------------------
    def __str__(self):
        estado = "Pagado" if self.pagado else "Pendiente"
        return f"Pago {self.mes} | Cliente {self.id_cliente} | {estado}"

    # ---------------------------------------------------------
    #   CONVERTIR A DICCIONARIO (para exportar o logs)
    # ---------------------------------------------------------
    def to_dict(self):
        return {
            "id_pago": self.id_pago,
            "id_cliente": self.id_cliente,
            "mes": self.mes,
            "fecha_generacion": self.fecha_generacion,
            "pagado": self.pagado,
            "fecha_pago": self.fecha_pago,
            "cuota": self.cuota,
            "metodo_pago": self.metodo_pago,
            "concepto": self.concepto
        }

    # ---------------------------------------------------------
    #   CREAR OBJETO DESDE DICCIONARIO
    # ---------------------------------------------------------
    @staticmethod
    def from_dict(data):
        return Pago(
            id_pago=data.get("id_pago"),
            id_cliente=data.get("id_cliente"),
            mes=data.get("mes", ""),
            fecha_generacion=data.get("fecha_generacion"),
            pagado=data.get("pagado", False),
            fecha_pago=data.get("fecha_pago"),
            cuota=data.get("cuota", 0.0),
            metodo_pago=data.get("metodo_pago"),
            concepto=data.get("concepto")
        )
