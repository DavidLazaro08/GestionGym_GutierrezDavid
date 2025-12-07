"""
---------------------------------------------------------
VENTANA PRINCIPAL
Interfaz principal del sistema tras iniciar sesión.
Incluye menú lateral y un área central donde se cargan
las distintas vistas: clientes, pagos, reservas y aparatos.
---------------------------------------------------------
"""

import tkinter as tk
from tkinter import messagebox
from data.gestor_bd import GestorBD
from excepciones import ErrorBaseDatos


class MainWindow:
    """Ventana principal con navegación entre módulos."""

    # ---------------------------------------------------------
    #   CONSTRUCTOR
    # ---------------------------------------------------------
    def __init__(self, root):
        """Inicializa la ventana principal del sistema."""
        self.root = root
        self.root.title("GymForTheMoment - Sistema de Gestión")

        # Inicializa la base de datos la primera vez
        self.inicializar_bd()

        self.vista_actual = None

        self.configurar_interfaz()

        # Vista inicial (Clientes)
        self.mostrar_clientes()

    # ---------------------------------------------------------
    #   BASE DE DATOS
    # ---------------------------------------------------------
    def inicializar_bd(self):
        """Crea las tablas necesarias si no existen y captura errores."""
        try:
            gestor = GestorBD()
            gestor.conectar()
            gestor.crear_tablas()
            gestor.desconectar()

        except ErrorBaseDatos as e:
            messagebox.showerror(
                "Error de Base de Datos",
                f"No se pudo inicializar la base de datos.\n\nDetalle:\n{e}"
            )
            self.root.destroy()

    # ---------------------------------------------------------
    #   INTERFAZ PRINCIPAL
    # ---------------------------------------------------------
    def configurar_interfaz(self):
        """Configura el menú lateral y el área central del programa."""

        # Limpiar ventana raíz (por si venimos del logout)
        for widget in self.root.winfo_children():
            widget.destroy()

        frame_principal = tk.Frame(self.root)
        frame_principal.pack(fill="both", expand=True)

        # -----------------------------
        # MENÚ LATERAL
        # -----------------------------
        frame_menu = tk.Frame(frame_principal, bg="#2c3e50", width=200)
        frame_menu.pack(side="left", fill="y")
        frame_menu.pack_propagate(False)

        tk.Label(
            frame_menu,
            text="GymForTheMoment",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#2c3e50",
            pady=20
        ).pack()

        tk.Frame(frame_menu, bg="#34495e", height=2).pack(fill="x", padx=10, pady=10)

        botones = [
            ("📋 Clientes", self.mostrar_clientes, "#3498db"),
            ("💰 Pagos", self.mostrar_pagos, "#f39c12"),
            ("📅 Reservas", self.mostrar_reservas, "#e74c3c"),
            ("🏋️ Aparatos", self.mostrar_aparatos, "#2ecc71"),
        ]

        for texto, comando, color in botones:
            tk.Button(
                frame_menu,
                text=texto,
                command=comando,
                font=("Arial", 11),
                bg=color,
                fg="white",
                width=18,
                height=2,
                cursor="hand2",
                relief="flat",
                anchor="w",
                padx=15
            ).pack(pady=5, padx=10)

        tk.Frame(frame_menu, bg="#2c3e50").pack(expand=True)

        tk.Button(
            frame_menu,
            text="🚪 Cerrar Sesión",
            command=self.cerrar_sesion,
            font=("Arial", 11),
            bg="#95a5a6",
            fg="white",
            width=18,
            height=2,
            cursor="hand2",
            relief="flat",
            anchor="w",
            padx=15
        ).pack(pady=10, padx=10, side="bottom")

        # -----------------------------
        # ÁREA DE CONTENIDO
        # -----------------------------
        self.frame_contenido = tk.Frame(frame_principal, bg="#ecf0f1")
        self.frame_contenido.pack(side="right", fill="both", expand=True)

    # ---------------------------------------------------------
    #   CAMBIO DE VISTAS
    # ---------------------------------------------------------
    def cambiar_vista(self, clase_vista):
        """Destruye vista actual y carga la nueva en el área central."""

        if self.vista_actual:
            self.vista_actual.destroy()

        try:
            self.vista_actual = clase_vista(self.frame_contenido, self)
            self.vista_actual.pack(fill="both", expand=True, padx=20, pady=20)

        except ErrorBaseDatos as e:
            messagebox.showerror(
                "Error cargando módulo",
                f"No se pudo cargar la vista.\n\nDetalle:\n{e}"
            )

    # ------- Accesos directos a cada módulo -------
    def mostrar_clientes(self):
        from view.cliente_view import ClienteView
        self.cambiar_vista(ClienteView)

    def mostrar_pagos(self):
        from view.pago_view import PagoView
        self.cambiar_vista(PagoView)

    def mostrar_reservas(self):
        from view.reserva_view import ReservaView
        self.cambiar_vista(ReservaView)

    def mostrar_aparatos(self):
        from view.aparato_view import AparatoView
        self.cambiar_vista(AparatoView)

    # ---------------------------------------------------------
    #   CERRAR SESIÓN
    # ---------------------------------------------------------
    def cerrar_sesion(self):
        """Vuelve a la pantalla de login tras confirmación."""
        if not messagebox.askyesno("Cerrar sesión", "¿Desea cerrar sesión?"):
            return

        if self.vista_actual:
            self.vista_actual.destroy()

        for widget in self.root.winfo_children():
            widget.destroy()

        from view.login_view import LoginView
        login = LoginView(self.root)
        login.pack(fill="both", expand=True)
