"""
---------------------------------------------------------
VISTA DE LOGIN
Pantalla inicial del sistema. Permite acceder al programa
validando usuario y contraseña. Incluye opción para
restablecer la clave del administrador.
---------------------------------------------------------
"""

import tkinter as tk
from tkinter import messagebox

from excepciones import ErrorLogin


class LoginView(tk.Frame):
    """Vista principal de acceso al sistema."""

    # ---------------------------------------------------------
    #   CONSTRUCTOR
    # ---------------------------------------------------------
    def __init__(self, parent):
        """Inicializa la vista de login."""
        super().__init__(parent)
        self.parent = parent

        self.configurar_interfaz()

    # ---------------------------------------------------------
    #   INTERFAZ
    # ---------------------------------------------------------
    def configurar_interfaz(self):
        """Crea y organiza los elementos visuales del login."""

        self.configure(bg="#ecf0f1")

        # Contenedor central
        frame_login = tk.Frame(self, bg="white", padx=40, pady=40)
        frame_login.place(relx=0.5, rely=0.5, anchor="center")

        # Título
        tk.Label(
            frame_login,
            text="GymForTheMoment",
            font=("Arial", 28, "bold"),
            fg="#2c3e50",
            bg="white"
        ).pack(pady=(0, 10))

        tk.Label(
            frame_login,
            text="Sistema de Gestión de Gimnasio",
            font=("Arial", 12),
            fg="#7f8c8d",
            bg="white"
        ).pack(pady=(0, 30))

        # Usuario
        tk.Label(frame_login, text="Usuario:", font=("Arial", 11),
                 fg="#2c3e50", bg="white").pack(anchor="w", pady=(10, 5))

        self.entry_usuario = tk.Entry(
            frame_login, font=("Arial", 11),
            width=30, relief="solid", borderwidth=1
        )
        self.entry_usuario.pack(pady=(0, 15))
        self.entry_usuario.focus()

        # Contraseña
        tk.Label(frame_login, text="Contraseña:", font=("Arial", 11),
                 fg="#2c3e50", bg="white").pack(anchor="w", pady=(0, 5))

        self.entry_password = tk.Entry(
            frame_login, font=("Arial", 11), width=30,
            show="●", relief="solid", borderwidth=1
        )
        self.entry_password.pack(pady=(0, 25))
        self.entry_password.bind("<Return>", lambda e: self.iniciar_sesion())

        # Botón iniciar sesión
        tk.Button(
            frame_login,
            text="Iniciar Sesión",
            command=self.iniciar_sesion,
            font=("Arial", 12, "bold"),
            bg="#3498db", fg="white",
            width=25, height=2,
            cursor="hand2", relief="flat"
        ).pack(pady=(0, 10))

        # Reset contraseña
        tk.Button(
            frame_login,
            text="¿Restablecer contraseña?",
            command=self.abrir_reset_password,
            font=("Arial", 9),
            bg="white", fg="#3498db",
            cursor="hand2", relief="flat", borderwidth=0
        ).pack(pady=(0, 10))

        # Info inferior
        tk.Label(
            frame_login,
            text="Versión 2.0 - Arquitectura Moderna",
            font=("Arial", 9),
            fg="#95a5a6",
            bg="white"
        ).pack(pady=(20, 0))

    # ---------------------------------------------------------
    #   VALIDACIÓN CREDENCIALES
    # ---------------------------------------------------------
    def validar_credenciales(self, usuario, password):
        """
        Comprueba usuario y contraseña contra la base de datos.
        Devuelve True o False, o lanza ErrorLogin si falla la BD.
        """
        from controller.usuario_controller import UsuarioController
        controller = UsuarioController()
        return controller.validar_login(usuario, password)

    # ---------------------------------------------------------
    #   PROCESO DE LOGIN
    # ---------------------------------------------------------
    def iniciar_sesion(self):
        """Evalúa los datos introducidos y accede a la ventana principal."""

        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()

        if not usuario or not password:
            messagebox.showwarning("Campos vacíos",
                                   "Por favor, ingresa usuario y contraseña.")
            return

        try:
            credenciales_ok = self.validar_credenciales(usuario, password)

        except ErrorLogin as e:
            # Error interno en el controlador o la base de datos
            messagebox.showerror(
                "Error interno",
                f"No se pudo validar el inicio de sesión.\n\nDetalle:\n{e}"
            )
            return

        if credenciales_ok:
            self.cargar_ventana_principal()
        else:
            messagebox.showerror("Error de autenticación",
                                 "Usuario o contraseña incorrectos.")
            self.entry_password.delete(0, tk.END)
            self.entry_password.focus()

    # ---------------------------------------------------------
    #   CAMBIO A LA VENTANA PRINCIPAL
    # ---------------------------------------------------------
    def cargar_ventana_principal(self):
        """Destruye el login y muestra la ventana principal."""
        from view.main_window import MainWindow

        self.destroy()
        MainWindow(self.parent)

    # ---------------------------------------------------------
    #   RESET DE CONTRASEÑA
    # ---------------------------------------------------------
    def abrir_reset_password(self):
        """Abre un cuadro para restablecer la contraseña del admin."""

        ventana_reset = tk.Toplevel(self.parent)
        ventana_reset.title("Restablecer Contraseña")
        ventana_reset.geometry("400x300")
        ventana_reset.configure(bg="white")
        ventana_reset.resizable(False, False)

        ventana_reset.transient(self.parent)
        ventana_reset.grab_set()

        # Título
        tk.Label(
            ventana_reset,
            text="Restablecer Contraseña de Admin",
            font=("Arial", 14, "bold"),
            fg="#2c3e50", bg="white"
        ).pack(pady=20)

        # Clave maestra
        tk.Label(
            ventana_reset, text="Clave Maestra:",
            font=("Arial", 11), fg="#2c3e50", bg="white"
        ).pack(pady=(10, 5))

        entry_clave = tk.Entry(
            ventana_reset, font=("Arial", 11),
            width=30, show="●"
        )
        entry_clave.pack(pady=(0, 15))
        entry_clave.focus()

        # Nueva contraseña
        tk.Label(
            ventana_reset,
            text="Nueva contraseña para Admin:",
            font=("Arial", 11), fg="#2c3e50", bg="white"
        ).pack(pady=(10, 5))

        entry_pass = tk.Entry(
            ventana_reset, font=("Arial", 11),
            width=30, show="●"
        )
        entry_pass.pack(pady=(0, 20))

        def procesar_reset():
            clave = entry_clave.get()
            nueva_pass = entry_pass.get()

            if clave != "RESET2025":
                messagebox.showerror("Error", "Clave maestra incorrecta.",
                                     parent=ventana_reset)
                return

            if not nueva_pass:
                messagebox.showwarning("Advertencia",
                                       "La nueva contraseña no puede estar vacía.",
                                       parent=ventana_reset)
                return

            from controller.usuario_controller import UsuarioController
            controller = UsuarioController()

            try:
                ok = controller.resetear_password("admin", nueva_pass)

            except ErrorLogin as e:
                messagebox.showerror(
                    "Error interno",
                    f"No se pudo actualizar la contraseña.\n\nDetalle:\n{e}",
                    parent=ventana_reset
                )
                return

            if ok:
                messagebox.showinfo("Éxito",
                                    "Contraseña actualizada correctamente.",
                                    parent=ventana_reset)
                ventana_reset.destroy()
            else:
                messagebox.showerror("Error",
                                     "No se pudo restablecer la contraseña.",
                                     parent=ventana_reset)

        tk.Button(
            ventana_reset,
            text="Restablecer",
            command=procesar_reset,
            font=("Arial", 11, "bold"),
            bg="#e74c3c", fg="white",
            width=20, cursor="hand2"
        ).pack(pady=10)
