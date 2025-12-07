"""
---------------------------------------------------------
CONTROLADOR DE CLIENTES
Gestiona la lógica relacionada con clientes del sistema.
Creación, lectura, actualización, eliminación y búsquedas.
---------------------------------------------------------
"""

from data.gestor_bd import GestorBD
from model.cliente import Cliente
from util.validaciones import validar_dni, validar_email, validar_telefono
from excepciones import ErrorBaseDatos, ErrorValidacion


class ClienteController:
    """Controlador encargado de gestionar clientes."""

    # ---------------------------------------------------------
    #   CONSTRUCTOR
    # ---------------------------------------------------------
    def __init__(self):
        """Inicializa el controlador y el gestor de BD."""
        self.db = GestorBD()

    # ---------------------------------------------------------
    #   CREAR CLIENTE
    # ---------------------------------------------------------
    def crear_cliente(self, nombre, apellidos, dni, email="", telefono="", fecha_alta=None):
        """
        Crea un nuevo cliente en estado activo (con validaciones previas).
        """
        # --- Validaciones simples ---
        if not validar_dni(dni):
            raise ErrorValidacion("DNI no válido.")

        if email and not validar_email(email):
            raise ErrorValidacion("Email no válido.")

        if telefono and not validar_telefono(telefono):
            raise ErrorValidacion("Teléfono no válido.")

        try:
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
            return nuevo_id

        except ErrorBaseDatos as e:
            raise ErrorBaseDatos(f"No se pudo crear el cliente: {e}")

        finally:
            self.db.desconectar()

    # ---------------------------------------------------------
    #   OBTENER CLIENTE POR ID
    # ---------------------------------------------------------
    def obtener_cliente(self, id_cliente):
        """Devuelve un cliente por su ID o None si no existe."""
        try:
            self.db.conectar()
            fila = self.db.obtener_datos(
                "SELECT * FROM Cliente WHERE id_cliente = ?",
                (id_cliente,)
            )

        except ErrorBaseDatos as e:
            raise ErrorBaseDatos(f"No se pudo obtener el cliente: {e}")

        finally:
            self.db.desconectar()

        if not fila:
            return None

        f = fila[0]
        return Cliente(*f)

    # ---------------------------------------------------------
    #   OBTENER TODOS LOS CLIENTES
    # ---------------------------------------------------------
    def obtener_todos_clientes(self):
        """Devuelve una lista con todos los clientes registrados."""
        try:
            self.db.conectar()
            filas = self.db.obtener_datos("SELECT * FROM Cliente")

        except ErrorBaseDatos as e:
            raise ErrorBaseDatos(f"No se pudo obtener la lista de clientes: {e}")

        finally:
            self.db.desconectar()

        return [Cliente(*f) for f in filas]

    # ---------------------------------------------------------
    #   ACTUALIZAR CLIENTE
    # ---------------------------------------------------------
    def actualizar_cliente(self, id_cliente, **kwargs):
        """
        Actualiza cualquier dato del cliente.
        """
        if not kwargs:
            return False

        # Validaciones si vienen ciertos campos
        if "dni" in kwargs and not validar_dni(kwargs["dni"]):
            raise ErrorValidacion("DNI no válido.")

        if "email" in kwargs and kwargs["email"] and not validar_email(kwargs["email"]):
            raise ErrorValidacion("Email no válido.")

        if "telefono" in kwargs and kwargs["telefono"] and not validar_telefono(kwargs["telefono"]):
            raise ErrorValidacion("Teléfono no válido.")

        try:
            self.db.conectar()
            ok = self.db.actualizar("Cliente", kwargs, f"id_cliente = {id_cliente}")
            return ok

        except ErrorBaseDatos as e:
            raise ErrorBaseDatos(f"No se pudo actualizar el cliente: {e}")

        finally:
            self.db.desconectar()

    # ---------------------------------------------------------
    #   ELIMINAR CLIENTE
    # ---------------------------------------------------------
    def eliminar_cliente(self, id_cliente):
        """Elimina un cliente del sistema."""
        try:
            self.db.conectar()
            ok = self.db.eliminar("Cliente", f"id_cliente = {id_cliente}")
            return ok

        except ErrorBaseDatos as e:
            raise ErrorBaseDatos(f"No se pudo eliminar el cliente: {e}")

        finally:
            self.db.desconectar()

    # ---------------------------------------------------------
    #   BUSCAR CLIENTES
    # ---------------------------------------------------------
    def buscar_clientes(self, criterio):
        """
        Busca clientes por nombre, apellidos o DNI.
        """
        patron = f"%{criterio}%"

        try:
            self.db.conectar()
            filas = self.db.obtener_datos(
                """
                SELECT * FROM Cliente
                WHERE nombre LIKE ? OR apellidos LIKE ? OR dni LIKE ?
                """,
                (patron, patron, patron)
            )

        except ErrorBaseDatos as e:
            raise ErrorBaseDatos(f"No se pudo realizar la búsqueda: {e}")

        finally:
            self.db.desconectar()

        return [Cliente(*f) for f in filas]
