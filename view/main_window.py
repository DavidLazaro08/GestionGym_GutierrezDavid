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
        """Crea las tablas necesarias si no existen y carga datos iniciales."""
        try:
            gestor = GestorBD()
            gestor.conectar()

            # Creamos las tablas si no existen
            gestor.crear_tablas()

            # Comprobamos si la tabla Cliente está vacía
            total_clientes = gestor.obtener_datos("SELECT COUNT(*) FROM Cliente")[0][0]

            if total_clientes == 0:
                # Ruta del archivo SQL que dejamos con datos iniciales
                import os
                ruta_sql = os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    "data",
                    "datos_iniciales.sql"
                )
                ruta_sql = os.path.abspath(ruta_sql)

                # Método para ejecutar archivo SQL
                try:
                    with open(ruta_sql, "r", encoding="utf-8") as f:
                        sql = f.read()
                    gestor.cursor.executescript(sql)
                    gestor.conexion.commit()
                    print("[INFO] Datos iniciales insertados correctamente.")
                except Exception as e:
                    print(f"[ERROR] No se pudieron insertar datos iniciales: {e}")

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

        frame_principal = tk.Frame(self.root, bg="#0a0d12")
        frame_principal.pack(fill="both", expand=True)

        # ---------------------------------------------------------
        # MENÚ LATERAL MODERNO CON DEGRADADO
        # ---------------------------------------------------------
        frame_menu = tk.Frame(frame_principal, bg="#1a2332", width=220)
        frame_menu.pack(side="left", fill="y")
        frame_menu.pack_propagate(False)

        # Canvas con degradado de fondo
        canvas_menu_bg = tk.Canvas(frame_menu, highlightthickness=0, bd=0)
        canvas_menu_bg.place(x=0, y=0, width=220, relheight=1.0)
        
        # Crear degradado vertical (de arriba a abajo)
        color_inicio = "#1a2332"
        color_final = "#0a0d12"
        
        r1, g1, b1 = int(color_inicio[1:3], 16), int(color_inicio[3:5], 16), int(color_inicio[5:7], 16)
        r2, g2, b2 = int(color_final[1:3], 16), int(color_final[3:5], 16), int(color_final[5:7], 16)
        
        steps = 200
        for i in range(steps):
            r = int(r1 + (r2-r1)*(i/steps))
            g = int(g1 + (g2-g1)*(i/steps))
            b = int(b1 + (b2-b1)*(i/steps))
            color = f"#{r:02x}{g:02x}{b:02x}"
            canvas_menu_bg.create_rectangle(0, i*3, 220, (i+1)*3, outline=color, fill=color)
        
        # Frame para contenido sobre el canvas
        content_menu = tk.Frame(frame_menu, bg="#1a2332")
        content_menu.place(x=0, y=0, width=220, relheight=1.0)

        # ---------------------------------------------------------
        # LOGO
        # ---------------------------------------------------------
        try:
            from PIL import Image, ImageTk
            from resources.style.colores import LOGO_TEXTO
            
            logo_img = Image.open(LOGO_TEXTO)
            w, h = logo_img.size
            new_w = 180
            new_h = int((new_w / w) * h)
            
            logo_img = logo_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            self.logo_sidebar = ImageTk.PhotoImage(logo_img)
            
            tk.Label(
                content_menu,
                image=self.logo_sidebar,
                bg="#1a2332"
            ).pack(pady=(20, 15))
            
        except Exception as e:
            # Fallback si no se encuentra el logo
            tk.Label(
                content_menu,
                text="GymForTheMoment",
                font=("Segoe UI", 14, "bold"),
                fg="#00d4aa",
                bg="#1a2332",
                pady=20
            ).pack()

        # Separador sutil
        tk.Frame(content_menu, bg="#2d3a4f", height=1).pack(fill="x", padx=15, pady=(0, 20))

        # ---------------------------------------------------------
        # BOTONES DE NAVEGACIÓN
        # ---------------------------------------------------------
        botones = [
            ("📋  Clientes", self.mostrar_clientes, "#00d4aa"),   # Cyan
            ("💰  Pagos", self.mostrar_pagos, "#3b82f6"),         # Azul
            ("📅  Reservas", self.mostrar_reservas, "#8b5cf6"),   # Morado
            ("🏋  Aparatos", self.mostrar_aparatos, "#ef4444"),   # Rojo
        ]

        for texto, comando, color in botones:
            # Canvas para el borde de color
            canvas = tk.Canvas(
                content_menu,
                width=220,
                height=48,
                bg="#1a2332",
                highlightthickness=0,
                bd=0
            )
            canvas.pack(pady=4, padx=0)
            
            # Borde izquierdo de color
            borde_id = canvas.create_rectangle(
                0, 0, 3, 48,
                fill=color,
                outline=""
            )
            
            # Fondo del botón (oscuro sutil)
            fondo_id = canvas.create_rectangle(
                3, 0, 220, 48,
                fill="#0f1419",
                outline=""
            )
            
            # Botón transparente sobre el canvas
            btn = tk.Button(
                canvas,
                text=texto,
                command=comando,
                font=("Segoe UI", 11, "bold"),
                bg="#0f1419",
                fg="#e2e8f0",
                relief="flat",
                cursor="hand2",
                anchor="w",
                padx=15,
                bd=0,
                activebackground="#2d3a4f",
                activeforeground="white"
            )
            btn.place(x=3, y=0, width=217, height=48)
            
            # Efectos hover
            def on_enter(e, c=canvas, fid=fondo_id, bid=borde_id, col=color, b=btn):
                c.itemconfig(fid, fill="#2d3a4f")
                c.itemconfig(bid, fill=self._aclarar_color(col))
                b.configure(bg="#2d3a4f", fg="white")
            
            def on_leave(e, c=canvas, fid=fondo_id, bid=borde_id, col=color, b=btn):
                c.itemconfig(fid, fill="#0f1419")
                c.itemconfig(bid, fill=col)
                b.configure(bg="#0f1419", fg="#e2e8f0")
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

        # Espaciador flexible
        tk.Frame(content_menu, bg="#1a2332").pack(expand=True)

        # ---------------------------------------------------------
        # BOTÓN CERRAR SESIÓN
        # ---------------------------------------------------------
        # Canvas para el botón de logout
        canvas_logout = tk.Canvas(
            content_menu,
            width=220,
            height=48,
            bg="#1a2332",
            highlightthickness=0,
            bd=0
        )
        canvas_logout.pack(pady=15, padx=0, side="bottom")
        
        # Fondo del botón (sin borde de color)
        fondo_logout_id = canvas_logout.create_rectangle(
            0, 0, 220, 48,
            fill="#0f1419",
            outline=""
        )
        
        btn_logout = tk.Button(
            canvas_logout,
            text="🚪 Cerrar Sesión",
            command=self.cerrar_sesion,
            font=("Segoe UI", 10, "bold"),
            bg="#0f1419",
            fg="#9ca3af",
            relief="flat",
            cursor="hand2",
            anchor="w",
            padx=15,
            bd=0,
            activebackground="#2d3a4f",
            activeforeground="white"
        )
        btn_logout.place(x=0, y=0, width=220, height=48)
        
        # Efectos hover para logout
        def on_logout_enter(e):
            canvas_logout.itemconfig(fondo_logout_id, fill="#2d3a4f")
            btn_logout.configure(bg="#2d3a4f", fg="#e2e8f0")
        
        def on_logout_leave(e):
            canvas_logout.itemconfig(fondo_logout_id, fill="#0f1419")
            btn_logout.configure(bg="#0f1419", fg="#9ca3af")
        
        btn_logout.bind("<Enter>", on_logout_enter)
        btn_logout.bind("<Leave>", on_logout_leave)

        # ---------------------------------------------------------
        # ÁREA DE CONTENIDO
        # ---------------------------------------------------------
        self.frame_contenido = tk.Frame(frame_principal, bg="#f5f7fa")
        self.frame_contenido.pack(side="right", fill="both", expand=True)

    # ---------------------------------------------------------
    #   FUNCIONES AUXILIARES PARA COLORES
    # ---------------------------------------------------------
    def _aclarar_color(self, hex_color):
        """Aclara un color hexadecimal para efecto hover."""
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r = min(255, int(r * 1.15))
        g = min(255, int(g * 1.15))
        b = min(255, int(b * 1.15))
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def _oscurecer_color(self, hex_color):
        """Oscurece un color hexadecimal para efecto active."""
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r = int(r * 0.85)
        g = int(g * 0.85)
        b = int(b * 0.85)
        return f"#{r:02x}{g:02x}{b:02x}"

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
