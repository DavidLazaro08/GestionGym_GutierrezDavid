"""
---------------------------------------------------------
CONTROLADOR DE USUARIOS
Gestiona la autenticación del sistema: login, creación y
reseteo de contraseñas. Usa hashing SHA-256 para mayor
seguridad.
---------------------------------------------------------
"""

import hashlib
from data.gestor_bd import GestorBD
from model.usuario import Usuario

# Excepciones del sistema
from excepciones import (
    ErrorLogin,
    ErrorBaseDatos,
    DBConsultaError,
    DBActualizacionError,
    DBInsercionError
)


class UsuarioController:
    """Controlador encargado de gestionar los usuarios del sistema."""

    # ---------------------------------------------------------
    #   CONSTRUCTOR
    # ---------------------------------------------------------
    def __init__(self):
        """Inicializa el gestor de base de datos."""
        self.gestor = GestorBD()

    # ---------------------------------------------------------
    #   HASH DE CONTRASEÑA
    # ---------------------------------------------------------
    def hash_password(self, password_claro):
        """Devuelve el hash SHA-256 de la contraseña recibida."""
        return hashlib.sha256(password_claro.encode()).hexdigest()

    # ---------------------------------------------------------
    #   CREAR USUARIO
    # ---------------------------------------------------------
    def crear_usuario(self, usuario, password_claro):
        """
        Crea un usuario nuevo con contraseña hasheada.
        Lanza ErrorLogin si algo falla.
        """
        try:
            self.gestor.conectar()
            password_hash = self.hash_password(password_claro)

            datos = {
                "usuario": usuario,
                "password_hash": password_hash
            }

            nuevo_id = self.gestor.insertar("Usuario", datos)
            return nuevo_id

        except (DBInsercionError, ErrorBaseDatos) as e:
            raise ErrorLogin(f"No se pudo crear el usuario: {e}")

        finally:
            self.gestor.desconectar()

    # ---------------------------------------------------------
    #   VALIDAR LOGIN
    # ---------------------------------------------------------
    def validar_login(self, usuario, password_claro):
        """
        Comprueba si el usuario existe y la contraseña es correcta.
        Devuelve True o False. Lanza ErrorLogin si hay fallos en la consulta.
        """
        try:
            self.gestor.conectar()

            query = """
                SELECT id_usuario, usuario, password_hash 
                FROM Usuario 
                WHERE usuario = ?
            """

            resultado = self.gestor.obtener_datos(query, (usuario,))

        except (DBConsultaError, ErrorBaseDatos) as e:
            raise ErrorLogin(f"Error al validar credenciales: {e}")

        finally:
            self.gestor.desconectar()

        # Usuario inexistente
        if not resultado:
            return False

        _, _, password_hash_bd = resultado[0]
        password_hash_ingresado = self.hash_password(password_claro)

        return password_hash_ingresado == password_hash_bd

    # ---------------------------------------------------------
    #   RESETEAR CONTRASEÑA
    # ---------------------------------------------------------
    def resetear_password(self, usuario, password_nueva):
        """
        Actualiza la contraseña del usuario indicado.
        Lanza ErrorLogin si ocurre un fallo en la BD.
        """
        try:
            self.gestor.conectar()

            password_hash = self.hash_password(password_nueva)
            datos = {"password_hash": password_hash}
            condicion = f"usuario = '{usuario}'"

            return self.gestor.actualizar("Usuario", datos, condicion)

        except (DBActualizacionError, ErrorBaseDatos) as e:
            raise ErrorLogin(f"No se pudo actualizar la contraseña: {e}")

        finally:
            self.gestor.desconectar()
