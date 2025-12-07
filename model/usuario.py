"""
Modelo de Usuario
Representa un usuario del sistema con credenciales de acceso
"""


class Usuario:
    """Clase que representa un usuario del sistema"""
    
    def __init__(self, id_usuario, usuario, password_hash):
        """
        Inicializa un usuario
        
        Args:
            id_usuario: ID único del usuario
            usuario: Nombre de usuario
            password_hash: Hash SHA-256 de la contraseña
        """
        self.id_usuario = id_usuario
        self.usuario = usuario
        self.password_hash = password_hash
    
    def __repr__(self):
        return f"Usuario(id={self.id_usuario}, usuario='{self.usuario}')"
