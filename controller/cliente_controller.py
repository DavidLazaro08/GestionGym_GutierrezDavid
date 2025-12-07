# ---------------------------------------------------------
#   CONTROLADOR DE CLIENTES
#   Gestiona la lógica relacionada con clientes del sistema.
# ---------------------------------------------------------

from data.gestor_bd import GestorBD
from model.cliente import Cliente


class ClienteController:

    def __init__(self):
        """Inicializa el controlador y el gestor de BD."""
        self.db = GestorBD()

    # ---------------------------------------------------------
    #   CREAR CLIENTE
    # ---------------------------------------------------------
    def crear_cliente(self, nombre, apellidos, dni, email="", telefono="", fecha_alta=None):
        """Crea un nuevo cliente activo en el sistema."""
        self.db.conectar()

        datos = {
            "nombre": nombre,
            "apellidos": apellidos,
            "dni": dni,
            "email": email,
            "telefono": telefono,
            "fecha_alta": fecha_alta,
            "estado": "activo"
        }

        nuevo_id = self.db.insertar("Cliente", datos)
        self.db.desconectar()
        return nuevo_id

    # ---------------------------------------------------------
    #   OBTENER CLIENTE POR ID
    # ---------------------------------------------------------
    def obtener_cliente(self, id_cliente):
        """Devuelve un cliente por su ID."""
        self.db.conectar()
        fila = self.db.obtener_datos(
            "SELECT * FROM Cliente WHERE id_cliente = ?",
            (id_cliente,)
        )
        self.db.desconectar()

        if not fila:
            return None

        f = fila[0]
        return Cliente(f[0], f[1], f[2], f[3], f[4], f[5], f[6], f[7])

    # ---------------------------------------------------------
    #   OBTENER TODOS LOS CLIENTES
    # ---------------------------------------------------------
    def obtener_todos_clientes(self):
        """Devuelve todos los clientes registrados."""
        self.db.conectar()
        filas = self.db.obtener_datos("SELECT * FROM Cliente")
        self.db.desconectar()

        return [Cliente(f[0], f[1], f[2], f[3], f[4], f[5], f[6], f[7]) for f in filas]

    # ---------------------------------------------------------
    #   ACTUALIZAR CLIENTE
    # ---------------------------------------------------------
    def actualizar_cliente(self, id_cliente, **kwargs):
        """Actualiza cualquier dato del cliente."""
        if not kwargs:
            return False

        self.db.conectar()
        actualizado = self.db.actualizar("Cliente", kwargs, f"id_cliente = {id_cliente}")
        self.db.desconectar()
        return actualizado

    # ---------------------------------------------------------
    #   ELIMINAR CLIENTE
    # ---------------------------------------------------------
    def eliminar_cliente(self, id_cliente):
        """Elimina un cliente del sistema."""
        self.db.conectar()
        ok = self.db.eliminar("Cliente", f"id_cliente = {id_cliente}")
        self.db.desconectar()
        return ok

    # ---------------------------------------------------------
    #   BUSCAR CLIENTES (nombre/apellidos/DNI)
    # ---------------------------------------------------------
    def buscar_clientes(self, criterio):
        """Busca clientes por nombre, apellidos o DNI."""
        patron = f"%{criterio}%"

        self.db.conectar()
        filas = self.db.obtener_datos(
            """
            SELECT * FROM Cliente 
            WHERE nombre LIKE ? OR apellidos LIKE ? OR dni LIKE ?
            """,
            (patron, patron, patron)
        )
        self.db.desconectar()

        return [Cliente(f[0], f[1], f[2], f[3], f[4], f[5], f[6], f[7]) for f in filas]
