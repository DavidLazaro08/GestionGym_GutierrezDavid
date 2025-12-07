"""
Módulo de excepciones del sistema.

Estas clases representan errores propios de la aplicación
y permiten distinguirlos de excepciones más genéricas.
Las mantenemos en un archivo independiente porque forman parte
de la arquitectura y pueden usarse desde cualquier parte.
"""

# ---------------------------------------------------------
# Excepciones generales del sistema
# ---------------------------------------------------------

class ErrorBaseDatos(Exception):
    """Error relacionado con operaciones de base de datos."""
    pass


class ErrorValidacion(Exception):
    """Error producido por datos no válidos o inconsistentes."""
    pass


class ErrorLogin(Exception):
    """Error en el proceso de autenticación."""
    pass


# ---------------------------------------------------------
# Excepciones específicas de la base de datos
# ---------------------------------------------------------

class DBConexionError(ErrorBaseDatos):
    """Error al conectar con la base de datos."""
    pass


class DBConsultaError(ErrorBaseDatos):
    """Error al realizar una consulta."""
    pass


class DBInsercionError(ErrorBaseDatos):
    """Error durante la inserción de datos."""
    pass


class DBActualizacionError(ErrorBaseDatos):
    """Error al actualizar datos."""
    pass


class DBEliminacionError(ErrorBaseDatos):
    """Error al eliminar datos."""
    pass
