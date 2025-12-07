"""
GymForTheMoment - Sistema de Gestión de Gimnasio
Punto de entrada principal de la aplicación
"""

import tkinter as tk
from view.login_view import LoginView
from data.gestor_bd import GestorBD


def main():
    """Función principal que inicia la aplicación"""

    # ---------------------------------------------------------
    #   INICIALIZAR BASE DE DATOS ANTES DE LOGIN
    # ---------------------------------------------------------
    gestor = GestorBD()
    gestor.conectar()
    gestor.crear_tablas()
    gestor.desconectar()

    # ---------------------------------------------------------
    #   INICIAR INTERFAZ
    # ---------------------------------------------------------
    root = tk.Tk()
    root.title("GymForTheMoment - Sistema de Gestión")
    root.geometry("1000x700")
    
    # Iniciar con la pantalla de login
    login = LoginView(root)
    login.pack(fill="both", expand=True)
    
    root.mainloop()


if __name__ == "__main__":
    main()
