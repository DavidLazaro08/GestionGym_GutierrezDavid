# ---------------------------------------------------------
#   CONTROLADOR DE APARATOS
#   Gestiona toda la lógica relacionada con los aparatos.
# ---------------------------------------------------------

from data.gestor_bd import GestorBD
from model.aparato import Aparato


class AparatoController:

    # ---------------------------------------------------------
    #   CONSTRUCTOR
    # ---------------------------------------------------------
    def __init__(self):
        """Inicializa el controlador y su gestor de BD."""
        self.db = GestorBD()

    # ---------------------------------------------------------
    #   CREAR APARATO
    # ---------------------------------------------------------
    def crear_aparato(self, nombre, tipo, descripcion="", estado="disponible"):
        """
        Inserta un aparato nuevo en la base de datos.
        """
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
    #   OBTENER APARATO POR ID
    # ---------------------------------------------------------
    def obtener_aparato(self, id_aparato):
        """Devuelve un objeto Aparato según su ID."""
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
        """Devuelve una lista de todos los aparatos registrados."""
        self.db.conectar()
        filas = self.db.obtener_datos("SELECT * FROM Aparato")
        self.db.desconectar()

        return [Aparato(f[0], f[1], f[2], f[3], f[4]) for f in filas]

    # ---------------------------------------------------------
    #   ACTUALIZAR APARATO
    # ---------------------------------------------------------
    def actualizar_aparato(self, id_aparato, nombre=None, tipo=None,
                           estado=None, descripcion=None):
        """
        Actualiza cualquier campo del aparato.
        """
        datos = {}

        if nombre is not None:
            datos["nombre"] = nombre
        if tipo is not None:
            datos["tipo"] = tipo
        if estado is not None:
            datos["estado"] = estado
        if descripcion is not None:
            datos["descripcion"] = descripcion

        if not datos:
            return False  # Nada que actualizar

        self.db.conectar()
        ok = self.db.actualizar("Aparato", datos, f"id_aparato = {id_aparato}")
        self.db.desconectar()
        return ok

    # ---------------------------------------------------------
    #   ELIMINAR APARATO
    # ---------------------------------------------------------
    def eliminar_aparato(self, id_aparato):
        """Elimina un aparato por ID."""
        self.db.conectar()
        ok = self.db.eliminar("Aparato", f"id_aparato = {id_aparato}")
        self.db.desconectar()
        return ok

    # ---------------------------------------------------------
    #   OBTENER APARATOS DISPONIBLES
    # ---------------------------------------------------------
    def obtener_aparatos_disponibles(self):
        """Devuelve todos los aparatos cuyo estado sea 'disponible'."""
        self.db.conectar()
        filas = self.db.obtener_datos(
            "SELECT * FROM Aparato WHERE estado = 'disponible'"
        )
        self.db.desconectar()

        return [Aparato(f[0], f[1], f[2], f[3], f[4]) for f in filas]

    # ---------------------------------------------------------
    #   OBTENER APARATOS POR TIPO
    # ---------------------------------------------------------
    def obtener_aparatos_por_tipo(self, tipo):
        """Filtra aparatos por su tipo."""
        self.db.conectar()
        filas = self.db.obtener_datos(
            "SELECT * FROM Aparato WHERE tipo = ?",
            (tipo,)
        )
        self.db.desconectar()

        return [Aparato(f[0], f[1], f[2], f[3], f[4]) for f in filas]
