# ---------------------------------------------------------
#   CONTROLADOR DE APARATOS
#   Lógica de negocio para gestionar aparatos del gimnasio
# ---------------------------------------------------------

from data.gestor_bd import GestorBD
from model.aparato import Aparato


class AparatoController:
    """Controlador encargado de gestionar los aparatos."""

    # ---------------------------------------------------------
    #   CONSTRUCTOR
    # ---------------------------------------------------------
    def __init__(self):
        self.db = GestorBD()

    # ---------------------------------------------------------
    #   CREAR APARATO
    # ---------------------------------------------------------
    def crear_aparato(self, nombre, tipo, descripcion="", estado="disponible"):
        """Crea un aparato nuevo en la base de datos."""
        self.db.conectar()

        datos = {
            "nombre": nombre,
            "tipo": tipo,
            "estado": estado,
            "descripcion": descripcion
        }

        nuevo_id = self.db.insertar("Aparato", datos)

        self.db.desconectar()
        return nuevo_id

    # ---------------------------------------------------------
    #   OBTENER UN APARATO POR ID
    # ---------------------------------------------------------
    def obtener_aparato(self, id_aparato):
        """Devuelve un aparato concreto según su ID."""
        self.db.conectar()
        filas = self.db.obtener_datos(
            "SELECT * FROM Aparato WHERE id_aparato = ?",
            (id_aparato,)
        )
        self.db.desconectar()

        if not filas:
            return None

        f = filas[0]
        return Aparato(f[0], f[1], f[2], f[3], f[4])

    # ---------------------------------------------------------
    #   OBTENER TODOS LOS APARATOS
    # ---------------------------------------------------------
    def obtener_todos_aparatos(self):
        """Devuelve la lista completa de aparatos registrados."""
        self.db.conectar()
        filas = self.db.obtener_datos("SELECT * FROM Aparato")
        self.db.desconectar()

        return [Aparato(f[0], f[1], f[2], f[3], f[4]) for f in filas]

    # ---------------------------------------------------------
    #   ACTUALIZAR APARATO
    # ---------------------------------------------------------
    def actualizar_aparato(self, id_aparato, nombre=None, tipo=None,
                           estado=None, descripcion=None):
        """Actualiza los datos de un aparato existente."""
        datos = {}

        if nombre is not None:
            datos["nombre"] = nombre
        if tipo is not None:
            datos["tipo"] = tipo
        if estado is not None:
            datos["estado"] = estado
        if descripcion is not None:
            datos["descripcion"] = descripcion

        # Si no se pasa ningún dato, no hace nada
        if not datos:
            return False

        self.db.conectar()
        ok = self.db.actualizar(
            "Aparato",
            datos,
            f"id_aparato = {id_aparato}"
        )
        self.db.desconectar()

        return ok

    # ---------------------------------------------------------
    #   ELIMINAR APARATO
    # ---------------------------------------------------------
    def eliminar_aparato(self, id_aparato):
        """Elimina un aparato por su ID."""
        self.db.conectar()
        ok = self.db.eliminar("Aparato", f"id_aparato = {id_aparato}")
        self.db.desconectar()

        return ok

    # ---------------------------------------------------------
    #   APARATOS DISPONIBLES
    # ---------------------------------------------------------
    def obtener_aparatos_disponibles(self):
        """Devuelve los aparatos cuyo estado sea 'disponible'."""
        self.db.conectar()
        filas = self.db.obtener_datos(
            "SELECT * FROM Aparato WHERE estado = 'disponible'"
        )
        self.db.desconectar()

        return [Aparato(f[0], f[1], f[2], f[3], f[4]) for f in filas]

    # ---------------------------------------------------------
    #   FILTRAR POR TIPO
    # ---------------------------------------------------------
    def obtener_aparatos_por_tipo(self, tipo):
        """Filtra los aparatos según su tipo."""
        self.db.conectar()
        filas = self.db.obtener_datos(
            "SELECT * FROM Aparato WHERE tipo = ?",
            (tipo,)
        )
        self.db.desconectar()

        return [Aparato(f[0], f[1], f[2], f[3], f[4]) for f in filas]
