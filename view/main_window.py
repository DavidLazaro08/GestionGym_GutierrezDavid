"""
---------------------------------------------------------
VENTANA PRINCIPAL
Interfaz principal del sistema tras iniciar sesión.
---------------------------------------------------------
"""

import tkinter as tk
from tkinter import messagebox
from data.gestor_bd import GestorBD
from excepciones import ErrorBaseDatos
from resources.style.colores import *

class MainWindow:
    """Ventana principal con navegación entre módulos."""

    def __init__(self, root):
        self.root = root
        self.root.title("GymForTheMoment - Sistema de Gestión")
        
        # Maximizar ventana si es posible, o tamaño grande por defecto
        try:
            self.root.state('zoomed')
        except:
            self.root.geometry("1400x900")
            
        self.root.configure(bg=COLOR_FONDO)

        self.inicializar_bd()
        self.vista_actual = None
        self.configurar_interfaz()
        
        # Vista inicial
        self.mostrar_clientes()

    def inicializar_bd(self):
        try:
            gestor = GestorBD()
            gestor.conectar()
            gestor.crear_tablas()
            
            # Insertar datos demo si está vacío
            if gestor.obtener_datos("SELECT COUNT(*) FROM Cliente")[0][0] == 0:
                import os
                ruta_sql = os.path.join(os.path.dirname(__file__), "..", "data", "datos_iniciales.sql")
                if os.path.exists(ruta_sql):
                    with open(ruta_sql, "r", encoding="utf-8") as f:
                        gestor.cursor.executescript(f.read())
                        gestor.conexion.commit()
            
            gestor.desconectar()
        except ErrorBaseDatos as e:
            messagebox.showerror("Error", f"Error de bases de datos: {e}")
            self.root.destroy()

    def configurar_interfaz(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Contenedor principal
        frame_principal = tk.Frame(self.root, bg=COLOR_FONDO)
        frame_principal.pack(fill="both", expand=True)

        # ---------------------------------------------------------
        # MENÚ LATERAL (Sidebar)
        # ---------------------------------------------------------
        frame_menu = tk.Frame(frame_principal, bg=COLOR_SIDEBAR_BG, width=ANCHO_SIDEBAR)
        frame_menu.pack(side="left", fill="y")
        frame_menu.pack_propagate(False)

        # Logo
        try:
            from PIL import Image, ImageTk
            img = Image.open(LOGO_TEXTO)
            w, h = img.size
            new_w = int(ANCHO_SIDEBAR * 0.8)
            new_h = int((new_w / w) * h)
            img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            self.logo_sidebar = ImageTk.PhotoImage(img)
            
            tk.Label(frame_menu, image=self.logo_sidebar, bg=COLOR_SIDEBAR_BG).pack(pady=(30, 20))
        except:
            tk.Label(
                frame_menu, text="GFTM", font=("Segoe UI", 20, "bold"),
                fg=COLOR_SECUNDARIO, bg=COLOR_SIDEBAR_BG
            ).pack(pady=(30, 20))

        # Separador neón
        tk.Frame(frame_menu, bg=COLOR_SECUNDARIO, height=1).pack(fill="x", padx=20, pady=(0, 30))

        # Botones de navegación
        self.contenedor_botones = tk.Frame(frame_menu, bg=COLOR_SIDEBAR_BG)
        self.contenedor_botones.pack(fill="x", padx=10)

        self._crear_boton_menu("👥  Clientes", self.mostrar_clientes)
        self._crear_boton_menu("💳  Pagos", self.mostrar_pagos)
        self._crear_boton_menu("📅  Reservas", self.mostrar_reservas)
        self._crear_boton_menu("🏋  Aparatos", self.mostrar_aparatos)

        # Botón Cerrar Sesión (Abajo)
        btn_logout = tk.Button(
            frame_menu,
            text="⏻ Cerrar Sesión",
            command=self.cerrar_sesion,
            font=("Segoe UI", 10),
            bg=COLOR_SIDEBAR_BG,
            fg="#ef4444",
            relief="flat",
            cursor="hand2",
            bd=0,
            activebackground="#2d1a1a",
            activeforeground="#ef4444"
        )
        btn_logout.pack(side="bottom", fill="x", pady=20)

        # ---------------------------------------------------------
        # ÁREA DE CONTENIDO
        # ---------------------------------------------------------
        self.frame_contenido = tk.Frame(frame_principal, bg=COLOR_FONDO)
        self.frame_contenido.pack(side="right", fill="both", expand=True)

    def _crear_boton_menu(self, texto, comando):
        btn = tk.Button(
            self.contenedor_botones,
            text=texto,
            command=comando,
            font=("Segoe UI", 11),
            bg=COLOR_SIDEBAR_BG,
            fg=COLOR_SIDEBAR_TEXT,
            relief="flat",
            cursor="hand2",
            anchor="w",
            padx=20,
            pady=10,
            bd=0,
            activebackground=COLOR_SIDEBAR_HOVER,
            activeforeground=COLOR_SECUNDARIO
        )
        btn.pack(fill="x", pady=2)
        
        # Efecto hover simple
        def on_enter(e):
            if e.widget['bg'] != COLOR_SIDEBAR_ACTIVE: # Si no está activo
                 e.widget['bg'] = COLOR_SIDEBAR_HOVER
                 e.widget['fg'] = COLOR_SECUNDARIO
        
        def on_leave(e):
             # Restaurar si no es la vista actual (lógica simplificada, se mejora con estado)
             e.widget['bg'] = COLOR_SIDEBAR_BG
             e.widget['fg'] = COLOR_SIDEBAR_TEXT
             
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def cambiar_vista(self, clase_vista):
        if self.vista_actual:
            self.vista_actual.destroy()
            
        try:
            # Instanciar nueva vista (pasando colores actualizados indirectamente por import)
            self.vista_actual = clase_vista(self.frame_contenido, self)
            self.vista_actual.pack(fill="both", expand=True, padx=30, pady=30)
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando vista: {e}")

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
        
    def cerrar_sesion(self):
        if messagebox.askyesno("Salir", "¿Cerrar sesión?"):
            self.root.destroy()
            # Aquí debería recargar el login, pero simplificamos destruyendo root del main
            # Para volver al login correctamente se requeriría reiniciar main.py o manejar ventanas
            import sys
            import os
            os.execl(sys.executable, sys.executable, *sys.argv)
