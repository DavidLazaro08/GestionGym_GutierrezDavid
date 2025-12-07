"""
GymForTheMoment - Sistema de Gestión de Gimnasio
Punto de entrada principal de la aplicación
"""

import tkinter as tk
from view.main_view import MainView


def main():
    """Función principal que inicia la aplicación"""
    root = tk.Tk()
    app = MainView(root)
    root.mainloop()


if __name__ == "__main__":
    main()
