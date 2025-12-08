"""
---------------------------------------------------------
VISTA DE LOGIN (mejorada + completa)
---------------------------------------------------------
"""

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from excepciones import ErrorLogin
from resources.style.colores import *


class LoginView(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Fondo degradado
        self._crear_degradado_fondo()

        # Widgets
        self.configurar_interfaz()

    # ---------------------------------------------------------
    #   FONDO DEGRADADO
    # ---------------------------------------------------------
    def _crear_degradado_fondo(self):
        """Crea un fondo degradado muy oscuro para contrastar con el contenedor."""
        self.canvas_bg = tk.Canvas(self, highlightthickness=0, bd=0)
        self.canvas_bg.pack(fill="both", expand=True)

        # Colores mucho más oscuros para mayor contraste
        color_inicio = "#1a2332"
        color_final = "#050709"

        r1, g1, b1 = self.winfo_rgb(color_inicio)
        r2, g2, b2 = self.winfo_rgb(color_final)

        r1//=256; g1//=256; b1//=256
        r2//=256; g2//=256; b2//=256

        steps = 400
        for i in range(steps):
            r = int(r1 + (r2-r1)*(i/steps))
            g = int(g1 + (g2-g1)*(i/steps))
            b = int(b1 + (b2-b1)*(i/steps))
            color = f"#{r:02x}{g:02x}{b:02x}"

            self.canvas_bg.create_rectangle(0, i*2, 2000, (i+1)*2,
                                            outline=color, fill=color)

        self.canvas_bg.bind("<Configure>", lambda e: self.lift())

    # ---------------------------------------------------------
    #   INTERFAZ
    # ---------------------------------------------------------
    def configurar_interfaz(self):
        """Crea la interfaz moderna del login con efectos visuales avanzados."""
        
        # ---------------------------------------------------------
        # SOMBRA DEL CONTENEDOR (simulada con capas)
        # ---------------------------------------------------------
        # Capa de sombra exterior (más difusa)
        shadow_outer = tk.Frame(self, bg="#0a0e14", width=470, height=660)
        shadow_outer.place(relx=0.5, rely=0.5, anchor="center")
        shadow_outer.pack_propagate(False)
        
        # Capa de sombra media
        shadow_mid = tk.Frame(self, bg="#0d1117", width=460, height=650)
        shadow_mid.place(relx=0.5, rely=0.5, anchor="center")
        shadow_mid.pack_propagate(False)
        
        # ---------------------------------------------------------
        # CONTENEDOR PRINCIPAL CON GLASSMORPHISM
        # ---------------------------------------------------------
        # Borde exterior con efecto glow sutil
        glow_border = tk.Frame(self, bg="#2a3f5f", width=452, height=642)
        glow_border.place(relx=0.5, rely=0.5, anchor="center")
        glow_border.pack_propagate(False)
        
        # Contenedor principal con efecto glassmorphism
        container = tk.Frame(glow_border, bg="#1a2332", width=450, height=640)
        container.place(relx=0.5, rely=0.5, anchor="center")
        container.pack_propagate(False)
        
        # Canvas para efectos de brillo sutil en el fondo
        canvas_shine = tk.Canvas(container, bg="#1a2332", highlightthickness=0, bd=0)
        canvas_shine.place(x=0, y=0, width=450, height=640)
        
        # Gradiente sutil de brillo
        for i in range(100):
            alpha = int(15 * (1 - i/100))
            color = f"#{alpha:02x}{alpha+10:02x}{alpha+20:02x}"
            canvas_shine.create_oval(-50, -50 + i*2, 200, 150 + i*2, 
                                    fill=color, outline="")
        
        # Frame para contenido sobre el canvas
        content_frame = tk.Frame(container, bg="#1a2332")
        content_frame.place(relx=0.5, rely=0.5, anchor="center", width=450, height=640)

        # ---------------------------------------------------------
        # LOGO
        # ---------------------------------------------------------
        try:
            logo_img = Image.open(LOGO_COMPLETO)
            w, h = logo_img.size
            new_w = 290
            new_h = int((new_w / w) * h)

            logo_img = logo_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_img)

            tk.Label(content_frame, image=self.logo_photo, bg="#1a2332")\
                .pack(pady=(10, 20))

        except Exception:
            tk.Label(content_frame, text="GymForTheMoment",
                     font=("Segoe UI", 24, "bold"),
                     fg=COLOR_SECUNDARIO,
                     bg="#1a2332").pack(pady=(10, 5))

        # ---------------------------------------------------------
        # TÍTULO CON EFECTO GLOW
        # ---------------------------------------------------------
        tk.Label(content_frame, text="Iniciar Sesión",
                 font=("Segoe UI", 22, "bold"),
                 fg="#ffffff", bg="#1a2332").pack(pady=(0, 4))

        tk.Label(content_frame, text="Accede a tu cuenta",
                 font=("Segoe UI", 10),
                 fg="#8b95a5", bg="#1a2332").pack(pady=(0, 20))

        # ---------------------------------------------------------
        # CAMPO USUARIO CON ICONO
        # ---------------------------------------------------------
        tk.Label(content_frame, text="USUARIO",
                 font=("Segoe UI", 9, "bold"),
                 fg="#a0aec0", bg="#1a2332",
                 anchor="w").pack(fill="x", padx=50, pady=(0, 8))

        # Frame con sombra para el campo
        user_shadow = tk.Frame(content_frame, bg="#0f1419", width=350, height=44)
        user_shadow.pack(padx=50, pady=(0, 0))
        user_shadow.pack_propagate(False)
        
        # Frame del campo con borde brillante
        frame_user_outer = tk.Frame(user_shadow, bg="#2d3a4f")
        frame_user_outer.place(relx=0.5, rely=0.5, anchor="center", width=350, height=42)
        
        frame_user = tk.Frame(frame_user_outer, bg="#0f1419")
        frame_user.place(relx=0.5, rely=0.5, anchor="center", width=348, height=40)

        # Contenedor horizontal para icono + entrada
        user_container = tk.Frame(frame_user, bg="#0f1419")
        user_container.pack(fill="both", expand=True)
        
        # Icono de usuario (centrado verticalmente)
        icon_user = tk.Label(user_container, text="👤", font=("Segoe UI", 14),
                            fg="#4a5568", bg="#0f1419")
        icon_user.pack(side="left", padx=(12, 8))
        
        self.entry_usuario = tk.Entry(
            user_container,
            font=("Segoe UI", 11),
            bg="#0f1419",
            fg="#ffffff",
            relief="flat",
            insertbackground=COLOR_SECUNDARIO,
            bd=0
        )
        self.entry_usuario.pack(side="left", fill="both", expand=True, padx=(0, 12))
        self.entry_usuario.focus()
        
        # Efecto focus (cambio de borde)
        def on_user_focus_in(e):
            frame_user_outer.configure(bg="#00d4aa")
        def on_user_focus_out(e):
            frame_user_outer.configure(bg="#2d3a4f")
        
        self.entry_usuario.bind("<FocusIn>", on_user_focus_in)
        self.entry_usuario.bind("<FocusOut>", on_user_focus_out)

        # ---------------------------------------------------------
        # CAMPO CONTRASEÑA CON ICONO
        # ---------------------------------------------------------
        tk.Label(content_frame, text="CONTRASEÑA",
                 font=("Segoe UI", 9, "bold"),
                 fg="#a0aec0", bg="#1a2332",
                 anchor="w").pack(fill="x", padx=50, pady=(18, 8))

        # Frame con sombra para el campo
        pass_shadow = tk.Frame(content_frame, bg="#0f1419", width=350, height=44)
        pass_shadow.pack(padx=50, pady=(0, 0))
        pass_shadow.pack_propagate(False)
        
        # Frame del campo con borde brillante
        frame_pass_outer = tk.Frame(pass_shadow, bg="#2d3a4f")
        frame_pass_outer.place(relx=0.5, rely=0.5, anchor="center", width=350, height=42)
        
        frame_pass = tk.Frame(frame_pass_outer, bg="#0f1419")
        frame_pass.place(relx=0.5, rely=0.5, anchor="center", width=348, height=40)

        # Contenedor horizontal para icono + entrada
        pass_container = tk.Frame(frame_pass, bg="#0f1419")
        pass_container.pack(fill="both", expand=True)
        
        # Icono de candado (centrado verticalmente)
        icon_lock = tk.Label(pass_container, text="🔒", font=("Segoe UI", 14),
                            fg="#4a5568", bg="#0f1419")
        icon_lock.pack(side="left", padx=(12, 8))
        
        self.entry_password = tk.Entry(
            pass_container,
            font=("Segoe UI", 11),
            bg="#0f1419",
            fg="#ffffff",
            show="●",
            relief="flat",
            insertbackground=COLOR_SECUNDARIO,
            bd=0
        )
        self.entry_password.pack(side="left", fill="both", expand=True, padx=(0, 12))
        self.entry_password.bind("<Return>", lambda e: self.iniciar_sesion())
        
        # Efecto focus
        def on_pass_focus_in(e):
            frame_pass_outer.configure(bg="#00d4aa")
        def on_pass_focus_out(e):
            frame_pass_outer.configure(bg="#2d3a4f")
        
        self.entry_password.bind("<FocusIn>", on_pass_focus_in)
        self.entry_password.bind("<FocusOut>", on_pass_focus_out)

        # ---------------------------------------------------------
        # BOTÓN LOGIN CON GRADIENTE Y HOVER
        # ---------------------------------------------------------
        # Canvas para simular gradiente en el botón
        btn_canvas = tk.Canvas(content_frame, width=350, height=45, 
                              bg="#1a2332", highlightthickness=0, bd=0)
        btn_canvas.pack(padx=50, pady=(25, 12))
        
        # Crear gradiente de cyan a verde
        for i in range(45):
            ratio = i / 45
            # De #00d4aa a #00b894
            r = int(0 + (0 - 0) * ratio)
            g = int(212 + (184 - 212) * ratio)
            b = int(170 + (148 - 170) * ratio)
            color = f"#{r:02x}{g:02x}{b:02x}"
            btn_canvas.create_rectangle(0, i, 350, i+1, fill=color, outline="")
        
        # Botón transparente sobre el canvas
        btn_login = tk.Button(
            btn_canvas,
            text="INICIAR SESIÓN",
            command=self.iniciar_sesion,
            font=("Segoe UI", 11, "bold"),
            bg="#00d4aa",
            fg="#0f1419",
            relief="flat",
            cursor="hand2",
            bd=0,
            activebackground="#00b894",
            activeforeground="#ffffff"
        )
        btn_login.place(relx=0.5, rely=0.5, anchor="center", width=350, height=45)
        
        # Efectos hover
        def on_btn_enter(e):
            btn_login.configure(bg="#00e6bb")
        def on_btn_leave(e):
            btn_login.configure(bg="#00d4aa")
        
        btn_login.bind("<Enter>", on_btn_enter)
        btn_login.bind("<Leave>", on_btn_leave)

        # ---------------------------------------------------------
        # RESET PASSWORD CON HOVER
        # ---------------------------------------------------------
        btn_reset = tk.Button(
            content_frame,
            text="¿Olvidaste tu contraseña?",
            command=self.abrir_reset_password,
            font=("Segoe UI", 9, "bold"),
            bg="#1a2332",
            fg="#8b5cf6",
            relief="flat",
            cursor="hand2",
            bd=0,
            activeforeground="#a78bfa"
        )
        btn_reset.pack(pady=(0, 8))
        
        def on_reset_enter(e):
            btn_reset.configure(fg="#a78bfa")
        def on_reset_leave(e):
            btn_reset.configure(fg="#8b5cf6")
        
        btn_reset.bind("<Enter>", on_reset_enter)
        btn_reset.bind("<Leave>", on_reset_leave)

        # ---------------------------------------------------------
        # FOOTER
        # ---------------------------------------------------------
        tk.Label(content_frame, 
                text="GFTM v2.0 · Gestiona tu Gym · © 2025 | by David Gutiérrez",
                font=("Segoe UI", 8),
                fg="#6c7280", bg="#1a2332").pack(pady=(8, 10))

    # ---------------------------------------------------------
    #   VALIDACIÓN CREDENCIALES
    # ---------------------------------------------------------
    def validar_credenciales(self, usuario, password):
        from controller.usuario_controller import UsuarioController
        controller = UsuarioController()
        return controller.validar_login(usuario, password)

    # ---------------------------------------------------------
    #   LOGIN
    # ---------------------------------------------------------
    def iniciar_sesion(self):
        """Evalúa los datos introducidos y accede a la ventana principal."""
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()

        if not usuario or not password:
            messagebox.showwarning(
                "Campos vacíos",
                "Por favor, ingresa usuario y contraseña."
            )
            return

        try:
            ok = self.validar_credenciales(usuario, password)
        except ErrorLogin as e:
            messagebox.showerror(
                "Error interno",
                f"No se pudo validar el inicio de sesión.\n\n{e}"
            )
            return

        if ok:
            self.cargar_ventana_principal()
        else:
            messagebox.showerror(
                "Error de autenticación",
                "Usuario o contraseña incorrectos."
            )
            self.entry_password.delete(0, tk.END)

    # ---------------------------------------------------------
    #   CARGAR MAIN
    # ---------------------------------------------------------
    def cargar_ventana_principal(self):
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
        ventana_reset.geometry("500x420")
        ventana_reset.configure(bg="#1a2332")
        ventana_reset.resizable(False, False)

        ventana_reset.transient(self.parent)
        ventana_reset.grab_set()

        # Centrar ventana
        ventana_reset.update_idletasks()
        x = (ventana_reset.winfo_screenwidth() // 2) - (500 // 2)
        y = (ventana_reset.winfo_screenheight() // 2) - (420 // 2)
        ventana_reset.geometry(f"500x420+{x}+{y}")

        # Contenedor principal
        container = tk.Frame(ventana_reset, bg="#1a2332")
        container.pack(expand=True, fill="both", padx=50, pady=40)

        # Título
        tk.Label(
            container,
            text="Restablecer Contraseña",
            font=("Segoe UI", 20, "bold"),
            fg="#ffffff",
            bg="#1a2332"
        ).pack(pady=(0, 8))

        tk.Label(
            container,
            text="Administrador del Sistema",
            font=("Segoe UI", 10),
            fg="#718096",
            bg="#1a2332"
        ).pack(pady=(0, 30))

        # ------------------------
        # Campo: Clave Maestra
        # ------------------------
        tk.Label(
            container,
            text="CLAVE MAESTRA",
            font=("Segoe UI", 9, "bold"),
            fg="#a0aec0",
            bg="#1a2332",
            anchor="w"
        ).pack(fill="x", pady=(0, 8))

        frame_master = tk.Frame(container, bg="#0f1419",
                                highlightthickness=1, highlightbackground="#2d3a4f")
        frame_master.pack(fill="x", pady=(0, 20))

        entry_clave = tk.Entry(
            frame_master,
            font=("Segoe UI", 11),
            bg="#0f1419",
            fg="#ffffff",
            show="●",
            relief="flat",
            insertbackground="#00d4aa",
            bd=0
        )
        entry_clave.pack(fill="x", padx=15, pady=10)
        entry_clave.focus()

        # ------------------------
        # Campo: Nueva Contraseña
        # ------------------------
        tk.Label(
            container,
            text="NUEVA CONTRASEÑA",
            font=("Segoe UI", 9, "bold"),
            fg="#a0aec0",
            bg="#1a2332",
            anchor="w"
        ).pack(fill="x", pady=(0, 8))

        frame_new = tk.Frame(container, bg="#0f1419",
                             highlightthickness=1, highlightbackground="#2d3a4f")
        frame_new.pack(fill="x", pady=(0, 30))

        entry_pass = tk.Entry(
            frame_new,
            font=("Segoe UI", 11),
            bg="#0f1419",
            fg="#ffffff",
            show="●",
            relief="flat",
            insertbackground="#00d4aa",
            bd=0
        )
        entry_pass.pack(fill="x", padx=15, pady=10)

        # ---------------------------------------------------------
        #   Lógica del reset
        # ---------------------------------------------------------
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

        # Botón restablecer
        tk.Button(
            container,
            text="RESTABLECER CONTRASEÑA",
            command=procesar_reset,
            font=("Segoe UI", 10, "bold"),
            bg="#ef4444",
            fg="#ffffff",
            width=28,
            height=2,
            cursor="hand2",
            relief="flat",
            bd=0,
            activebackground="#dc2626"
        ).pack()
