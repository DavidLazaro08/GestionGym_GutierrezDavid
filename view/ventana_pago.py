import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from util.helpers import formatear_cuota
from util.validaciones import validar_fecha
from resources.style.colores import *

class VentanaPago(tk.Toplevel):

    def __init__(self, master, pago, callback_confirmacion):
        super().__init__(master)
        self.title("Registrar Pago")
        self.geometry("420x440") 
        self.resizable(False, False)
        self.configure(bg=COLOR_FONDO)

        self.pago = pago
        self.callback = callback_confirmacion

        self.configurar_interfaz()

    def configurar_interfaz(self):

        # Título
        tk.Label(
            self, 
            text="Registrar Pago",
            font=("Segoe UI", 18, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_SECUNDARIO
        ).pack(pady=(20, 15))

        # Contenedor central
        frame = tk.Frame(self, bg=COLOR_FONDO)
        frame.pack(pady=5, padx=30, fill="x")

        # ---------------------------------------
        # DATOS INFORMATIVOS (solo lectura)
        # ---------------------------------------
        self._crear_label_info(frame, "Cliente:", 0)
        self._crear_label_valor(frame, self.pago["cliente"], 0)

        self._crear_label_info(frame, "Mes:", 1)
        self._crear_label_valor(frame, self.pago["mes"], 1)

        self._crear_label_info(frame, "Cuota:", 2)
        self._crear_label_valor(frame, formatear_cuota(self.pago["cuota"]), 2)

        # ---------------------------------------
        # CAMPOS EDITABLES
        # ---------------------------------------
        self._crear_label_info(frame, "Método de pago:", 3)
        
        self.combo_metodo = ttk.Combobox(
            frame,
            values=["efectivo", "tarjeta", "transferencia", "bizum"],
            state="readonly",
            width=22,
            font=("Segoe UI", 10)
        )
        self.combo_metodo.current(0)
        self.combo_metodo.grid(row=3, column=1, pady=8, sticky="w")

        self._crear_label_info(frame, "Fecha de pago:", 4)
        
        self.entry_fecha = tk.Entry(
            frame, 
            width=24,
            bg=COLOR_INPUT_BG,
            fg="white",
            insertbackground="white",
            relief="flat",
            font=("Segoe UI", 10),
            bd=5
        )
        self.entry_fecha.insert(0, str(date.today()))
        self.entry_fecha.grid(row=4, column=1, pady=8, sticky="w")

        self._crear_label_info(frame, "Concepto:", 5)
        
        self.text_concepto = tk.Text(
            frame, 
            width=24, 
            height=3,
            bg=COLOR_INPUT_BG,
            fg="white",
            insertbackground="white",
            relief="flat",
            font=("Segoe UI", 10),
            bd=5
        )
        self.text_concepto.insert("1.0", "Cuota mensual")
        self.text_concepto.grid(row=5, column=1, pady=8, sticky="w")

        # ---------------------------------------
        # BOTONES
        # ---------------------------------------
        frame_btn = tk.Frame(self, bg=COLOR_FONDO)
        frame_btn.pack(pady=25)

        self._crear_boton(
            frame_btn, "Confirmar pago", self.confirmar, COLOR_EXITO
        ).grid(row=0, column=0, padx=10)

        self._crear_boton(
            frame_btn, "Cancelar", self.destroy, COLOR_PELIGRO
        ).grid(row=0, column=1, padx=10)

    # ---------------------------------------------------------
    # HELPERS VISUALES
    # ---------------------------------------------------------
    def _crear_label_info(self, parent, text, row):
        tk.Label(
            parent,
            text=text,
            font=("Segoe UI", 10, "bold"),
            bg=COLOR_FONDO,
            fg="#A9B4C6" # Gris claro
        ).grid(row=row, column=0, sticky="w", pady=5, padx=(0, 10))

    def _crear_label_valor(self, parent, text, row):
        tk.Label(
            parent,
            text=text,
            font=("Segoe UI", 10),
            bg=COLOR_FONDO,
            fg="white"
        ).grid(row=row, column=1, sticky="w", pady=5)

    def _crear_boton(self, parent, text, command, color):
        btn = tk.Button(
            parent,
            text=text,
            bg=color,
            fg="white" if color != COLOR_SECUNDARIO else "#151C25", # Texto oscuro si el fondo es turquesa brillante
            activebackground="white",
            activeforeground=color,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            command=command,
            width=15,
            pady=5
        )
        
        # Hover effect
        def on_enter(e):
            btn["bg"] = self._lighten_color(color)
        def on_leave(e):
            btn["bg"] = color
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
        
    def _lighten_color(self, color):
        # Mapeo rapido para hover
        if color == COLOR_EXITO: return "#33e0c0"
        if color == COLOR_PELIGRO: return "#ff7676"
        return color

    # ---------------------------------------------------------
    # VALIDACIÓN Y CONFIRMACIÓN
    # ---------------------------------------------------------
    def confirmar(self):
        metodo = self.combo_metodo.get()
        fecha = self.entry_fecha.get()
        concepto = self.text_concepto.get("1.0", "end").strip()

        # VALIDACIÓN 1 — Método obligatorio
        if not metodo:
            messagebox.showerror("Error", "Debe seleccionar un método de pago.")
            return

        # VALIDACIÓN 2 — Fecha válida
        if not validar_fecha(fecha):
            messagebox.showerror(
                "Fecha inválida",
                "La fecha debe tener formato YYYY-MM-DD."
            )
            return

        # VALIDACIÓN 3 — Concepto no vacío
        if concepto == "":
            concepto = "Cuota mensual"

        # Envío de datos a PagoView
        self.callback(metodo, fecha, concepto)

        # Cerrar ventana
        self.destroy()
